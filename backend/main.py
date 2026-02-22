from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .caption import router as caption_router
from .catdog import router as catdog_router
from .object import router as object_router
from .ocr import router as ocr_router
from .emotionage import router as emotionage_router
from .photoshop import router as photoshop_router   # 🆕 Photoshop Import

app = FastAPI(title="Multi Model Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(caption_router, prefix="/caption")
app.include_router(catdog_router, prefix="/catdog")
app.include_router(object_router, prefix="/object")
app.include_router(ocr_router, prefix="/ocr")
app.include_router(emotionage_router, prefix="/emotion")
app.include_router(photoshop_router, prefix="/photoshop")   # 🆕 Photoshop Route

@app.get("/")
def home():
    return {"message": "🔥 backend running with Photoshop Filters!"}
