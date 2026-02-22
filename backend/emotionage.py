from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import boto3
import os
import cv2
import numpy as np
import base64

router = APIRouter()

# AWS keys from environment (HuggingFace Secrets)
AWS_KEY = os.getenv("AKIA4O**********")                   # use your own key for amazon rekognition service
AWS_SECRET = os.getenv("mdTZ2Dht3UWmCh**************")    # use you own secrets for amazon rekognition service
AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")

client = boto3.client(
    "rekognition",
    aws_access_key_id=AWS_KEY,
    aws_secret_access_key=AWS_SECRET,
    region_name=AWS_REGION
)


def img_to_b64(img):
    _, buf = cv2.imencode(".jpg", img)
    return base64.b64encode(buf).decode("utf-8")


@router.post("/analyze")
async def analyze_face(file: UploadFile = File(...)):
    if "image" not in file.content_type:
        return JSONResponse({"error": "Only image files allowed!"}, status_code=400)

    # Read uploaded image
    img_bytes = await file.read()

    # Decode and keep a working copy
    npimg = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    if img is None:
        return JSONResponse({"error": "Invalid image"}, status_code=400)

    h, w, _ = img.shape

    # Call Rekognition
    try:
        response = client.detect_faces(
            Image={"Bytes": img_bytes},
            Attributes=["ALL"]
        )
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

    faces = response.get("FaceDetails", [])

    if not faces:
        return JSONResponse({
            "output": img_to_b64(img),
            "face_count": 0,
            "faces": [],
            "message": "⚠️ No faces detected."
        })

    results = []
    for f in faces:
        # Top emotion
        emotions = f.get("Emotions", [])
        top_emotion = max(emotions, key=lambda x: x["Confidence"]) if emotions else None

        # Bounding box
        box = f.get("BoundingBox", {})
        if box:
            x1 = int(box["Left"] * w)
            y1 = int(box["Top"] * h)
            x2 = int((box["Left"] + box["Width"]) * w)
            y2 = int((box["Top"] + box["Height"]) * h)

            # Rectangle
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Emotion label
            if top_emotion:
                label = top_emotion["Type"]
                cv2.putText(
                    img,
                    label,
                    (x1, max(0, y1 - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )

        # Append ordered result
        results.append({
            "top_emotion": top_emotion,
            "all_emotions": emotions,
            "gender": f.get("Gender", {}).get("Value", "Unknown"),
            "gender_conf": f.get("Gender", {}).get("Confidence", 0),
            "age_range": f.get("AgeRange", {}),
            "smile": f.get("Smile", {}),
            "eyes_open": f.get("EyesOpen", {}),
            "mouth_open": f.get("MouthOpen", {}),
            "eyeglasses": f.get("Eyeglasses", {}),
            "sunglasses": f.get("Sunglasses", {}),
            "beard": f.get("Beard", {}),
            "mustache": f.get("Mustache", {})
        })

    # Convert edited image to Base64
    edited_b64 = img_to_b64(img)

    return JSONResponse({
        "output": edited_b64,
        "face_count": len(results),
        "faces": results
    })

