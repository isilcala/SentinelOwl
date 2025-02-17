import os
import cv2
import numpy as np
import onnxruntime as ort
from typing import Tuple, Dict, Any


def load_model(model_path: str) -> ort.InferenceSession:
    """Load ONNX model with validation"""
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    return ort.InferenceSession(model_path, providers=["CPUExecutionProvider"])


def get_model_metadata(model: ort.InferenceSession) -> Dict[str, Any]:
    """Get ONNX model input metadata"""
    input_info = model.get_inputs()[0]
    return {
        "name": input_info.name,
        "shape": input_info.shape,
        "dtype": input_info.type,
    }


def preprocess_frame(frame: np.ndarray, model_metadata: Dict[str, Any]) -> np.ndarray:
    """Dynamic preprocessing based on model input"""
    input_shape = model_metadata["shape"]
    _, c, h, w = input_shape  # 假设输入形状为 [batch, channel, height, width]

    # 颜色空间转换
    if c == 1:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    elif c == 3:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    else:
        raise ValueError(f"Unsupported channel number: {c}")

    # 尺寸调整
    frame = cv2.resize(frame, (w, h))

    # 数据类型转换
    if model_metadata["dtype"] == "tensor(float)":
        frame = frame.astype(np.float32) / 255.0
    elif model_metadata["dtype"] == "tensor(uint8)":
        frame = frame.astype(np.uint8)
    else:
        raise ValueError(f"Unsupported dtype: {model_metadata['dtype']}")

    # 维度调整
    if c > 1:
        frame = np.transpose(frame, (2, 0, 1))  # HWC to CHW
    else:
        frame = np.expand_dims(frame, axis=0)  # Add channel dim

    return np.expand_dims(frame, axis=0)  # Add batch dim


def predict(model: ort.InferenceSession, frame: np.ndarray) -> Tuple[int, float]:
    """Run inference with dynamic input handling"""
    input_name = model.get_inputs()[0].name
    output = model.run(None, {input_name: frame})
    probabilities = np.squeeze(output[0])
    predicted_class = int(np.argmax(probabilities))
    confidence = float(np.max(probabilities))
    return predicted_class, confidence


def main(camera_url: str, model_path: str):
    """Main validation function"""
    # URL 验证
    if not camera_url.startswith(("http://", "rtsp://", "file://")):
        raise ValueError(f"Invalid camera URL: {camera_url}")

    # 加载模型
    model = load_model(model_path)
    model_metadata = get_model_metadata(model)
    print(f"Model input requirements:\n{model_metadata}")

    # 打开摄像头
    cap = cv2.VideoCapture(camera_url)
    if not cap.isOpened():
        print(f"❌ Failed to open camera: {camera_url}")
        return

    try:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to capture frame")
            return

        # 动态预处理
        processed_frame = preprocess_frame(frame, model_metadata)
        print(f"Processed frame shape: {processed_frame.shape}")

        # 推理
        class_id, confidence = predict(model, processed_frame)
        print(f"Predicted class: {class_id}, Confidence: {confidence:.4f}")

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
