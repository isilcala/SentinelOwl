import cv2
import numpy as np
import onnxruntime as ort
from typing import Tuple


def load_model(model_path: str) -> ort.InferenceSession:
    """Load the ONNX model"""
    try:
        session = ort.InferenceSession(model_path, providers=["CPUExecutionProvider"])
        print(f"✅ Model loaded successfully: {model_path}")
        return session
    except Exception as e:
        print(f"❌ Failed to load model from {model_path}: {str(e)}")
        raise


def preprocess_frame(
    frame: np.ndarray, target_size: Tuple[int, int] = (28, 28)
) -> np.ndarray:
    """Preprocess the input frame for MNIST model"""
    # Convert to grayscale
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Resize to model input size
    frame = cv2.resize(frame, target_size)
    # Normalize to [0, 1]
    frame = frame.astype(np.float32) / 255.0
    # Add batch and channel dimensions
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
    """Main validation function"""
    # Load model
    model = load_model(model_path)
    print(f"✅ Model loaded: {model_path}")

    # Open camera stream
    cap = cv2.VideoCapture(camera_url)
    if not cap.isOpened():
        print(f"❌ Failed to open camera: {camera_url}")
        return

    print(f"✅ Camera connected: {camera_url}")

    try:
        # Capture a single frame
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to capture frame")
            return

        # Preprocess and predict
        processed_frame = preprocess_frame(frame)
        predicted_class, confidence = predict(model, processed_frame)
        print(f"🔍 Predicted class: {predicted_class}, Confidence: {confidence:.4f}")

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
