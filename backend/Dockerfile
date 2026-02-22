FROM python:3.10-slim

# Prevent Python from writing pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# System deps (added Tesseract OCR + language pack)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    tesseract-ocr \
    libtesseract-dev \
    tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/*

# Create working dir
WORKDIR /app

# Copy dependency lists
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy FastAPI app
COPY app ./app

# Ensure tesseract path available (optional env for pytesseract)
ENV TESSERACT_PATH=/usr/bin/tesseract

# Expose FastAPI port
EXPOSE 7860

# Run uvicorn when container starts
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
