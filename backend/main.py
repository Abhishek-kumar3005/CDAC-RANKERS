import os
import numpy as np
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from keras.applications.vgg16 import VGG16, preprocess_input
from keras.preprocessing.image import load_img, img_to_array
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
import uvicorn

# =========================================================
#  CONFIG
# =========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "..", "models")

MODEL_PATH = os.path.join(MODEL_DIR, "caption_model_best.keras")
TOKEN_PATH = os.path.join(MODEL_DIR, "tokenizer.pkl")
MAXLEN_PATH = os.path.join(MODEL_DIR, "max_length.pkl")
VOCAB_SIZE_PATH = os.path.join(MODEL_DIR, "vocab_size.pkl")

# =========================================================
#  LOAD MODEL + METADATA
# =========================================================
import pickle

print("🔹 Loading model and metadata...")
model = load_model(MODEL_PATH)

with open(TOKEN_PATH, "rb") as f:
    tokenizer = pickle.load(f)

with open(MAXLEN_PATH, "rb") as f:
    max_length = pickle.load(f)

with open(VOCAB_SIZE_PATH, "rb") as f:
    vocab_size = pickle.load(f)

print("✅ Model loaded successfully!")

# =========================================================
#  VGG16 FEATURE EXTRACTOR (FC2 = 4096)
# =========================================================
vgg = VGG16(include_top=True, weights="imagenet")
# use FC2 output
from keras.models import Model
vgg = Model(inputs=vgg.inputs, outputs=vgg.layers[-2].output)


def extract_features(image_array):
    """
    image_array is already (224,224,3)
    """
    image = np.expand_dims(image_array, axis=0)
    image = preprocess_input(image)
    feature = vgg.predict(image, verbose=0)
    return feature  # shape (1,4096)


# =========================================================
#  INDEX <-> WORD HELPERS
# =========================================================
def idx_to_word(integer, tokenizer):
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None


# =========================================================
#  BEAM SEARCH
# =========================================================
def predict_caption_beam(model, image, tokenizer, max_length, beam_size=5):
    # sequence format: [tokens, score, sentence]
    sequences = [[[], 0.0, "startseq"]]

    for _ in range(max_length):
        all_candidates = []
        for seq, score, text in sequences:
            if text.endswith(" endseq"):
                all_candidates.append((seq, score, text))
                continue

            # convert text → integer seq
            integer_seq = tokenizer.texts_to_sequences([text])[0]
            integer_seq = pad_sequences([integer_seq], maxlen=max_length, padding='post')

            # prediction
            yhat = model.predict([image, integer_seq], verbose=0)[0]

            # top beam words
            top_indices = np.argsort(yhat)[-beam_size:]

            for idx in top_indices:
                word = idx_to_word(idx, tokenizer)
                if word is None:
                    continue
                new_text = text + " " + word
                new_seq = seq + [idx]
                new_score = score + np.log(yhat[idx] + 1e-10)
                all_candidates.append((new_seq, new_score, new_text))

        # keep best beams
        ordered = sorted(all_candidates, key=lambda tup: tup[1], reverse=True)
        sequences = ordered[:beam_size]

    best = sequences[0][2]
    best = best.replace("startseq", "").replace("endseq", "").strip()
    return best


# =========================================================
#  FASTAPI APP
# =========================================================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Image Caption Backend Running"}


@app.post("/predict-caption")
async def predict_caption(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        # convert raw image → numpy
        from PIL import Image
        import io
        img = Image.open(io.BytesIO(contents)).convert("RGB")
        img = img.resize((224, 224))
        img = img_to_array(img)

        # extract CNN feature
        feature = extract_features(img)

        # beam search caption
        caption = predict_caption_beam(
            model,
            feature,
            tokenizer,
            max_length,
            beam_size=5,
        )

        return {"caption": caption}

    except Exception as e:
        return {"error": str(e)}


# =========================================================
#  START SERVER (WHEN RUN LOCALLY)
# =========================================================
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=7860)

