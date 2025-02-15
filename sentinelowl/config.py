from pydantic import BaseModel


class CameraConfig(BaseModel):
    """Configuration for camera input"""

    url: str = "http://localhost:8080/?action=stream"
    type: str = "mjpeg"  # or "rtsp"
    reconnect_interval: int = 5


class DetectionConfig(BaseModel):
    """Configuration for defect detection"""

    interval: int = 5  # Detection interval in seconds
    warning_threshold: float = 0.7
    critical_threshold: float = 0.85


class ModelConfig(BaseModel):
    """Configuration for AI models"""

    type: str = "placeholder"  # Model type (e.g., "placeholder", "onnx")
    warning_threshold: float = 0.7
    critical_threshold: float = 0.85


class AppConfig(BaseModel):
    """Main application configuration"""

    camera: CameraConfig = CameraConfig()
    detection: DetectionConfig = DetectionConfig()
    model: ModelConfig = ModelConfig()
