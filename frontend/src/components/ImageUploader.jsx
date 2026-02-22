import { useState, useRef } from "react";

export default function ImageUploader({ title, onFileSelect }) {
  const [image, setImage] = useState(null);
  const dropRef = useRef(null);

  const handleFile = (file) => {
    if (!file) return;

    // Allow only images
    if (!file.type.startsWith("image/")) {
      alert("❌ Only image files allowed!");
      return;
    }

    // 10MB size limit
    if (file.size > 10 * 1024 * 1024) {
      alert("❌ Max image size is 10MB!");
      return;
    }

    setImage(URL.createObjectURL(file));
    onFileSelect(file);
  };

  const handleUpload = (e) => {
    const file = e.target.files[0];
    handleFile(file);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    dropRef.current.style.borderColor = "#ccc";
    const file = e.dataTransfer.files[0];
    handleFile(file);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    dropRef.current.style.borderColor = "#007AFF";
  };

  const handleDragLeave = () => {
    dropRef.current.style.borderColor = "#ccc";
  };

  const resetImage = () => {
    setImage(null);
    onFileSelect(null);
  };

  return (
    <div style={{ marginTop: "30px" }}>
      <h3 style={{ opacity: 0.7 }}>{title}</h3>

      {!image && (
        <div
          ref={dropRef}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => document.getElementById("uploadInput").click()}
          style={{
            border: "2px dashed #ccc",
            borderRadius: "14px",
            padding: "30px",
            textAlign: "center",
            cursor: "pointer",
            transition: "0.3s",
          }}
        >
          <p style={{ opacity: 0.6 }}>Drag & Drop image here</p>
          <p style={{ opacity: 0.5 }}>or</p>

          <input
            id="uploadInput"
            type="file"
            accept="image/*"
            onChange={handleUpload}
            style={{ display: "none" }}
          />

          <button
            style={{
              padding: "8px 14px",
              borderRadius: "8px",
              border: "none",
              background: "#007AFF",
              color: "#fff",
              marginTop: "10px",
              cursor: "pointer",
            }}
            onClick={(e) => {
              e.stopPropagation();
              document.getElementById("uploadInput").click();
            }}
          >
            Upload Image
          </button>
        </div>
      )}

      {image && (
        <div style={{ textAlign: "center" }}>
          <img
            src={image}
            alt="preview"
            style={{
              width: "100%",
              marginTop: "20px",
              borderRadius: "10px",
            }}
          />

          <button
            onClick={resetImage}
            style={{
              marginTop: "15px",
              padding: "8px 14px",
              borderRadius: "8px",
              border: "none",
              background: "#FF3B30",
              color: "white",
              cursor: "pointer",
            }}
          >
            Remove Image
          </button>
        </div>
      )}
    </div>
  );
}
