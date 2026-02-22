from fastapi import APIRouter, UploadFile, File
import numpy as np
from PIL import Image
from huggingface_hub import hf_hub_download
from keras.applications.vgg16 import VGG16, preprocess_input
from keras.models import load_model, Model
import io

router = APIRouter()

# HuggingFace Repo Configuration
REPO_ID = "Aakrosh3005/Aakroshmachinelearning"
MODEL_FILE = "catdog/catdog.keras"

# Download model from Hub
model_path = hf_hub_download(repo_id=REPO_ID, filename=MODEL_FILE)

# Feature extractor (VGG16)
vgg_base = VGG16(weights="imagenet", include_top=False, input_shape=(224, 224, 3))
feature_model = Model(inputs=vgg_base.input, outputs=vgg_base.output)

# Classifier model
clf = load_model(model_path)

def extract_features(img):
    arr = np.expand_dims(img, axis=0)
    arr = preprocess_input(arr)
    feat = feature_model.predict(arr, verbose=0)
    feat = feat.flatten().reshape(1, -1)
    return feat

@router.post("/predict")
async def predict_catdog(file: UploadFile = File(...)):
    contents = await file.read()
    img = Image.open(io.BytesIO(contents)).convert("RGB")
    img = img.resize((224, 224))
    img = np.array(img)

    feat = extract_features(img)
    prob = float(clf.predict(feat)[0][0])
    label = "DOG" if prob > 0.5 else "CAT"

    return {
        "label": label,
        "probability": prob
    }
