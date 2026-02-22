from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import cv2
import numpy as np
import base64
import traceback

router = APIRouter()

# -------------------------
# Utils
# -------------------------
def img_to_b64(img):
    _, buf = cv2.imencode(".jpg", img)
    return base64.b64encode(buf).decode("utf-8")

def read_image(file_bytes):
    arr = np.frombuffer(file_bytes, np.uint8)
    return cv2.imdecode(arr, cv2.IMREAD_COLOR)


# -------------------------
# 🔥 Portrait Enhancement Filter (replaces cartoon)
# -------------------------
def portrait_enhance(img):
    h, w = img.shape[:2]

    # slightly smaller for speed
    small = cv2.resize(img, (w//2, h//2))
    smooth = cv2.bilateralFilter(small, 15, 75, 75)

    # color richness
    hsv = cv2.cvtColor(smooth, cv2.COLOR_BGR2HSV)
    hsv[:,:,1] = cv2.add(hsv[:,:,1], 12)
    hsv[:,:,2] = cv2.add(hsv[:,:,2], 12)
    vibe = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    vibe = cv2.resize(vibe, (w, h))

    # background blur
    blur = cv2.GaussianBlur(vibe, (45,45), 18)

    gray = cv2.cvtColor(vibe, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 60, 120)
    mask = cv2.dilate(edges, None, iterations=3)
    mask = cv2.GaussianBlur(mask, (61,61), 15)
    mask = cv2.normalize(mask, None, 0, 1, cv2.NORM_MINMAX)

    mask3 = cv2.cvtColor((mask*255).astype(np.uint8), cv2.COLOR_GRAY2BGR)
    
    merged = cv2.addWeighted(vibe, mask, blur, 1-mask, 0)

    # clarity pop
    sharp = cv2.GaussianBlur(merged, (0,0), 3)
    final = cv2.addWeighted(merged, 1.5, sharp, -0.5, 0)

    return final


# -------------------------
# 🧊 Cool Blue Tint (replaces pencil_color)
# -------------------------
def cool_blue_tint(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    hsv[:,:,0] = cv2.add(hsv[:,:,0], 25)  # shift hue → blue
    hsv[:,:,1] = cv2.add(hsv[:,:,1], 35)  # more saturation
    hsv[:,:,2] = cv2.subtract(hsv[:,:,2], 10)  # a little dark cool
    
    blue = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    blue = cv2.bilateralFilter(blue, 9, 60, 60)  # smooth icy look
    blue = cv2.addWeighted(blue, 1.1, img, -0.1, 0)  # clean highlight

    return blue


# -------------------------
# Pencil Gray
# -------------------------
def pencil_gray(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inv = 255 - gray
    blur = cv2.GaussianBlur(inv, (21, 21), 0)
    sketch = cv2.divide(gray, 255 - blur, scale=256)
    return cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)


# -------------------------
# HDR + POP ART + B&W Film
# -------------------------
def hdr(img):
    return cv2.detailEnhance(img, sigma_s=15, sigma_r=0.15)

def pop_art(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv[:,:,1] = cv2.add(hsv[:,:,1], 80)
    hsv[:,:,2] = cv2.add(hsv[:,:,2], 25)
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def bw(img):
    b,g,r = cv2.split(img)
    film = (0.3*r + 0.59*g + 0.11*b).astype(np.uint8)
    return cv2.cvtColor(film, cv2.COLOR_GRAY2BGR)


# -------------------------
# Final Filter Map
# -------------------------
FILTERS = {
    "cartoon": portrait_enhance,     # ⚡ changed
    "pencil_gray": pencil_gray,
    "pencil_color": cool_blue_tint,  # ⚡ changed
    "hdr": hdr,
    "popart": pop_art,
    "bw": bw,
}


# -------------------------
# API Route
# -------------------------
@router.post("/filter")
async def apply_filter(style: str, file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()

        if style not in FILTERS:
            return JSONResponse({"error": "Invalid style"}, status_code=400)

        img = read_image(file_bytes)
        out = FILTERS[style](img)

        return JSONResponse({
            "style": style,
            "output": img_to_b64(out),
            "format": "jpg",
            "message": f"{style} applied"
        })

    except Exception as e:
        return JSONResponse({
            "error": str(e),
            "trace": traceback.format_exc()
        }, status_code=500)
