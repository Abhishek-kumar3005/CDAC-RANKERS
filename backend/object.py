from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse, JSONResponse
from huggingface_hub import hf_hub_download
from ultralytics import YOLO
import cv2, numpy as np, base64, tempfile, json, random

router = APIRouter()

# ================= MODEL LOAD ================= #
yolo_path = hf_hub_download(
    repo_id="Aakrosh3005/Aakroshmachinelearning",
    filename="object/yolov8n.pt"
)
model = YOLO(yolo_path)


def image_to_base64(img):
    _, buffer = cv2.imencode(".jpg", img)
    return base64.b64encode(buffer).decode("utf-8")


# ================= API ROUTE ================= #
@router.post("/detect")
async def detect_object(file: UploadFile = File(...)):
    content_type = file.content_type

    # ------------- IMAGE HANDLING ------------- #
    if "image" in content_type:
        img_bytes = await file.read()
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        results = model(img, verbose=False)[0]
        class_counts = {}

        for box in results.boxes:
            conf = float(box.conf[0])
            if conf < 0.40:
                continue  # skip low confidence

            cls_id = int(box.cls[0])
            cls_name = results.names[cls_id]

            # per-class numbering
            class_counts[cls_name] = class_counts.get(cls_name, 0) + 1
            obj_number = class_counts[cls_name]

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # random color
            color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            )

            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
            cv2.putText(
                img,
                f"{cls_name}-{obj_number}",
                (x1, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
                2
            )

        b64 = image_to_base64(img)

        return JSONResponse({
            "output": b64,
            "total_objects": sum(class_counts.values()),
            "counts": class_counts
        })

    # ------------- VIDEO HANDLING (FPS BOOST) ------------- #
    if "video" in content_type:
        temp_in = tempfile.NamedTemporaryFile(delete=True, suffix=".mp4")
        temp_out = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")

        temp_in.write(await file.read())
        temp_in.flush()

        cap = cv2.VideoCapture(temp_in.name)
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = None
        class_counts = {}

        frame_index = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_index += 1

            # ⏩ Skip frames for speed (50%)
            if frame_index % 2 != 0:
                continue

            # ⚡ Reduce resolution for faster CPU inference
            results = model(frame, imgsz=360, verbose=False)[0]

            for box in results.boxes:
                conf = float(box.conf[0])
                if conf < 0.40:
                    continue  # skip low confidence

                cls_id = int(box.cls[0])
                cls_name = results.names[cls_id]

                class_counts[cls_name] = class_counts.get(cls_name, 0) + 1
                obj_number = class_counts[cls_name]

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                # random color
                color = (
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255)
                )

                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(
                    frame,
                    f"{cls_name}-{obj_number}",
                    (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    color,
                    2
                )

            if out is None:
                h, w = frame.shape[:2]
                out = cv2.VideoWriter(temp_out.name, fourcc, 20, (w, h))

            out.write(frame)

        cap.release()
        out.release()

        headers = {
            "X-Object-Counts": json.dumps(class_counts)
        }

        return StreamingResponse(
            open(temp_out.name, "rb"),
            media_type="video/mp4",
            headers=headers
        )

    return {"error": "Unsupported file type!"}
