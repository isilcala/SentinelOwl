import os
import cv2
import numpy as np
import onnxruntime as ort
from typing import Tuple


def load_model(model_path: str) -> ort.InferenceSession:
    """Load the ONNX model with path validation"""
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    print(f"Loading model from: {model_path}")
    return ort.InferenceSession(model_path, providers=["CPUExecutionProvider"])


def preprocess_frame(
    frame: np.ndarray, target_size: Tuple[int, int] = (28, 28)
) -> np.ndarray:
    """Preprocess the input frame for MNIST model"""
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.resize(frame, target_size)
    frame = frame.astype(np.float32) / 255.0
    frame = np.expand_dims(frame, axis=(0, 1))  # Shape: (1, 1, 28, 28)
    return frame


def predict(model: ort.InferenceSession, frame: np.ndarray) -> Tuple[int, float]:
    """Run inference on the input frame"""
    input_name = model.get_inputs()[0].name
    output = model.run(None, {input_name: frame})
    probabilities = np.squeeze(output[0])  # Shape: (10,)
    predicted_class = int(np.argmax(probabilities))
    confidence = float(np.max(probabilities))
    return predicted_class, confidence


def main(camera_url: str, model_path: str):
    """Main validation function with URL validation"""
    if not camera_url.startswith(("http://", "rtsp://", "file://")):
        raise ValueError(f"Invalid camera URL: {camera_url}")

    # Load model
    model = load_model(model_path)

    # Open camera stream
    print(f"Connecting to camera: {camera_url}")
    cap = cv2.VideoCapture(camera_url)
    if not cap.isOpened():
        print(f"Failed to open camera: {camera_url}")
        return

    try:
        # Capture a single frame
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            return

        # Preprocess and predict
        processed_frame = preprocess_frame(frame)
        predicted_class, confidence = predict(model, processed_frame)
        print(f"Predicted class: {predicted_class}, Confidence: {confidence:.4f}")

    finally:
        cap.release()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Validate camera and model integration"
    )
    parser.add_argument("--camera-url", required=True, help="URL of the camera stream")
    parser.add_argument("--model-path", required=True, help="Path to the ONNX model")
    args = parser.parse_args()

    main(args.camera_url, args.model_path)
