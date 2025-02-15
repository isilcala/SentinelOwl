import time
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import NamedTuple
from ..config import AppConfig
from .camera import CameraHandler  # 新增关键导入
from .detector import DefectDetector
from .performance import PerformanceMonitor


class SentinelOwl:
    """Main application class for print monitoring"""

    def __init__(self, config: AppConfig):
        self.config = config
        self.camera = CameraHandler(config.camera)
        self.detector = DefectDetector(config.detection)
        self.executor = ThreadPoolExecutor(max_workers=2)
        self.performance = PerformanceMonitor()

    async def run(self):
        """Asynchronous monitoring loop"""
        try:
            while True:
                await self._monitor_step()
                await asyncio.sleep(self.config.detection.interval)
                self._log_performance()
        except asyncio.CancelledError:
            print("🦉 SentinelOwl shutdown gracefully.")
        finally:
            self.camera.release()

    def _log_performance(self):
        """Log performance statistics"""
        stats = self.performance.get_stats()
        print(
            f"📊 Performance: {stats.fps:.1f} FPS, "
            f"Processing Time: {stats.processing_time:.3f}s"
        )

    async def _monitor_step(self):
        """Single monitoring step"""
        frame = self.camera.capture_frame()
        if frame is not None:
            result = self.detector.analyze(frame)
            self._handle_result(result)

    def _handle_result(self, result):
        """Handle detection results"""
        if result.is_critical:
            self._trigger_emergency_stop()
        elif result.is_warning:
            self._notify_warning(result)

    def _trigger_emergency_stop(self):
        """Trigger emergency stop procedure"""
        print("🛑 Emergency stop: Critical defect detected!")

    def _notify_warning(self, result):
        """Notify about potential defects"""
        print(
            f"⚠️ Warning: Potential defect detected (confidence: {result.confidence:.2f})"
        )
