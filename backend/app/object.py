from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from huggingface_hub import hf_hub_download
from ultralytics import YOLO
import cv2, numpy as np, base64, random

router = APIRouter()

yolo_path = hf_hub_download(
    repo_id="Aakrosh3005/Aakroshmachinelearning",
    filename="object/yolov8n.pt"
)
model = YOLO(yolo_path)

def image_to_base64(img):
    _, buffer = cv2.imencode(".jpg", img)
    return base64.b64encode(buffer).decode("utf-8")

@router.post("/detect")
async def detect_object(file: UploadFile = File(...)):
    if "image" not in file.content_type:
        return {"error": "Only image allowed!"}

    img_bytes = await file.read()
    img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)

    results = model(img, imgsz=480, conf=0.35, verbose=False)[0]

    class_counts = {}

    for box in results.boxes:
        cls_id = int(box.cls[0])
        cls_name = results.names[cls_id]

        class_counts[cls_name] = class_counts.get(cls_name, 0) + 1
        obj_number = class_counts[cls_name]

        x1, y1, x2, y2 = map(int, box.xyxy[0])

        color = (
            random.randint(0,255),
            random.randint(0,255),
            random.randint(0,255)
        )
        cv2.rectangle(img, (x1,y1), (x2,y2), color, 2)
        cv2.putText(img, f"{cls_name}-{obj_number}", (x1,y1-5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    b64 = image_to_base64(img)

    return JSONResponse({
        "output": b64,
        "total_objects": sum(class_counts.values()),
        "counts": class_counts
    })
