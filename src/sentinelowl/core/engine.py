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

    def __init__(self, config):
        self.config = config
        self.camera = CameraHandler(config.camera)
        self.detector = DefectDetector(config.model)
        self.printer = PrinterController()
        self.plugin = AIGuardPlugin(config)

    async def run(self):
        """Start monitoring and plugin services"""
        await asyncio.gather(self._monitor_loop(), self._serve_plugin())

    def _log_performance(self):
        """Log performance statistics"""
        stats = self.performance.get_stats()
        print(
            f"📊 Performance: {stats.fps:.1f} FPS, "
            f"Processing Time: {stats.processing_time:.3f}s"
        )

    async def _monitor_loop(self):
        """Continuous monitoring loop"""
        while True:
            frame = await self.camera.capture_frame()
            if frame is not None:
                result = await self.detector.analyze(frame)
                self._handle_result(result)
            await asyncio.sleep(1 / self.config.camera.fps)

    async def _serve_plugin(self):
        """Start Moonraker plugin service"""
        # TODO: Implement plugin server
        pass

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
