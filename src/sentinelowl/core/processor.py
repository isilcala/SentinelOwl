import asyncio
from typing import Optional
import cv2
from .camera import CameraHandler
from .detector import DefectDetector


class FrameProcessor:
    """Continuous frame processing engine"""

    def __init__(self, config):
        self.camera = CameraHandler(config.camera)
        self.detector = DefectDetector(config.model)
        self._running = False

    async def start(self):
        """Start continuous processing"""
        self._running = True
        while self._running:
            frame = await self._capture_frame()
            if frame is not None:
                result = await self._analyze_frame(frame)
                self._handle_result(result)
            await asyncio.sleep(1 / config.camera.fps)

    async def _capture_frame(self) -> Optional[np.ndarray]:
        """Asynchronous frame capture"""
        return await asyncio.get_event_loop().run_in_executor(
            None, self.camera.capture_frame
        )

    async def _analyze_frame(self, frame: np.ndarray) -> dict:
        """Asynchronous frame analysis"""
        return await asyncio.get_event_loop().run_in_executor(
            None, self.detector.analyze, frame
        )

    def _handle_result(self, result: dict):
        """Handle detection results"""
        if result["critical"]:
            print(f"🛑 CRITICAL DEFECT! Confidence: {result['confidence']:.2f}")
        elif result["warning"]:
            print(f"⚠️ Warning: Confidence {result['confidence']:.2f}")
