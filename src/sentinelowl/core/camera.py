import cv2
import time
from typing import Optional, Tuple
from ..config import CameraConfig


class CameraConnectionError(Exception):
    """Custom exception for camera connection errors"""

    pass


class CameraHandler:
    """Handler for camera input"""

    def __init__(self, config: CameraConfig):
        self._retry_count = 0
        self.max_retries = 3  # ✅ 新增最大重试次数
        self.config = config
        self.cap = None
        self._initialize_camera()

    def _initialize_camera(self):
        """Initialize the camera connection"""
        try:
            self.cap = cv2.VideoCapture(self.config.url)
            if not self.cap.isOpened():
                raise RuntimeError(f"Failed to open camera: {self.config.url}")
            print(f"🟢 Camera connected: {self.config.url}")
        except Exception as e:
            print(f"🔴 Camera initialization failed: {str(e)}")
            self.cap = None

    def capture_frame(self) -> Optional[Tuple[bool, any]]:
        """Capture a single frame from the video stream"""
        if self.cap is None:
            self._reconnect_camera()
            if self.cap is None:
                return None

        ret, frame = self.cap.read()
        if not ret:
            print("⚠️ Frame capture failed, attempting to reconnect...")
            self._reconnect_camera()
            return None

        return frame

    def _reconnect_camera(self):
        if self._retry_count >= self.max_retries:
            raise CameraConnectionError(
                f"Failed to reconnect after {self.max_retries} attempts"
            )

        self._retry_count += 1
        """Attempt to reconnect to the camera"""
        if self.cap is not None:
            self.cap.release()

        print(
            f"Attempting to reconnect to camera in {self.config.reconnect_interval} seconds..."
        )
        time.sleep(self.config.reconnect_interval)
        self._initialize_camera()

    def release(self):
        """Release the camera resources"""
        if self.cap is not None:
            self.cap.release()
            print("Camera resources released.")
