from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import pytesseract
import cv2
import numpy as np
import base64

router = APIRouter()

def img_to_b64(img):
    _, buf = cv2.imencode(".jpg", img)
    return base64.b64encode(buf).decode("utf-8")


@router.post("/read")
async def read_text(file: UploadFile = File(...)):
    content_type = file.content_type

    if "image" not in content_type:
        return JSONResponse({"error": "Only image files allowed!"}, status_code=400)

    # Read image bytes → numpy array
    img_bytes = await file.read()
    npimg = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # Convert to grayscale & threshold (improves text results)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Run OCR
    raw_text = pytesseract.image_to_string(gray)

    # Prepare formatted output
    lines = [line.strip() for line in raw_text.split("\n") if line.strip()]
    result_text = "\n".join(lines) if lines else "⚠️ No readable text found"

    b64 = img_to_b64(img)

    return JSONResponse({
        "output": b64,         # return same image so UI can preview
        "text": result_text,   # extracted OCR text
        "line_count": len(lines)
    })
