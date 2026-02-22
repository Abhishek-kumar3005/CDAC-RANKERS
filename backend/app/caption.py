from fastapi import APIRouter, UploadFile, File
import numpy as np
from keras.applications.vgg16 import VGG16, preprocess_input
from keras.preprocessing.image import img_to_array
from keras.models import load_model, Model
from keras.preprocessing.sequence import pad_sequences
from huggingface_hub import hf_hub_download
from PIL import Image
import pickle, io

router = APIRouter()

# HuggingFace Repo Info
REPO_ID = "Aakrosh3005/Aakroshmachinelearning"
FOLDER = "models"

# File names inside HuggingFace repo
MODEL_FILE = f"{FOLDER}/caption_model_best.keras"
TOKEN_FILE = f"{FOLDER}/tokenizer.pkl"
MAXLEN_FILE = f"{FOLDER}/max_length.pkl"
VOCAB_FILE = f"{FOLDER}/vocab_size.pkl"

# Download all files
model_path = hf_hub_download(repo_id=REPO_ID, filename=MODEL_FILE)
token_path = hf_hub_download(repo_id=REPO_ID, filename=TOKEN_FILE)
maxlen_path = hf_hub_download(repo_id=REPO_ID, filename=MAXLEN_FILE)
vocab_path = hf_hub_download(repo_id=REPO_ID, filename=VOCAB_FILE)

# Load model & metadata
model = load_model(model_path)
tokenizer = pickle.load(open(token_path, "rb"))
max_length = pickle.load(open(maxlen_path, "rb"))
vocab_size = pickle.load(open(vocab_path, "rb"))

# VGG Extractor
vgg = VGG16(include_top=True, weights="imagenet")
vgg = Model(inputs=vgg.inputs, outputs=vgg.layers[-2].output)


def extract_features(img_array):
    arr = np.expand_dims(img_array, axis=0)
    arr = preprocess_input(arr)
    return vgg.predict(arr, verbose=0)


def idx_to_word(integer):
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None


def predict_caption_beam(image, beam_size=5):
    sequences = [[[], 0.0, "startseq"]]

    for _ in range(max_length):
        all_candidates = []
        for seq, score, sentence in sequences:
            if sentence.endswith(" endseq"):
                all_candidates.append((seq, score, sentence))
                continue

            integers = tokenizer.texts_to_sequences([sentence])[0]
            padded = pad_sequences([integers], maxlen=max_length, padding='post')

            yhat = model.predict([image, padded], verbose=0)[0]
            top_idx = np.argsort(yhat)[-beam_size:]

            for idx in top_idx:
                word = idx_to_word(idx)
                if not word:
                    continue

                new_sentence = sentence + " " + word
                new_seq = seq + [idx]
                new_score = score + np.log(yhat[idx] + 1e-10)
                all_candidates.append((new_seq, new_score, new_sentence))

        ordered = sorted(all_candidates, key=lambda tup: tup[1], reverse=True)
        sequences = ordered[:beam_size]

    best = sequences[0][2]
    best = best.replace("startseq", "").replace("endseq", "").strip()
    return best


@router.post("/predict")
async def predict_caption(file: UploadFile = File(...)):
    contents = await file.read()
    img = Image.open(io.BytesIO(contents)).convert("RGB")
    img = img.resize((224, 224))
    img = img_to_array(img)

    features = extract_features(img)
    caption = predict_caption_beam(features)

    return {"caption": caption}
