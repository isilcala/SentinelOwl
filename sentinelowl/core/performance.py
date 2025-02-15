import time
from dataclasses import dataclass
from typing import Deque
from collections import deque

@dataclass
class PerformanceStats:
    """Performance statistics"""
    fps: float
    processing_time: float
    frame_queue_size: int

class PerformanceMonitor:
    """Performance monitoring handler"""

    def __init__(self, window_size: int = 10):
        self.window_size = window_size
        self.frame_times: Deque[float] = deque(maxlen=window_size)
        self.processing_times: Deque[float] = deque(maxlen=window_size)
        self.start_time = time.time()

    def start_frame(self):
        """Record the start of a frame"""
        self.frame_times.append(time.time())

    def end_frame(self):
        """Record the end of a frame"""
        self.processing_times.append(time.time() - self.frame_times[-1])


    def get_stats(self) -> PerformanceStats:
        """Calculate performance statistics"""
        if len(self.frame_times) < 2:
            return PerformanceStats(fps=0.0, processing_time=0.0, frame_queue_size=0)

        # 计算时间窗口内的帧率
        time_window = self.frame_times[-1] - self.frame_times[0]
        if time_window <= 0:
            fps = 0.0
        else:
            fps = (len(self.frame_times) - 1) / time_window  # N个时间间隔对应 N-1 个帧

        # 计算平均处理时间
        avg_processing_time = sum(self.processing_times) / len(self.processing_times) if self.processing_times else 0.0

        return PerformanceStats(
            fps=fps,
            processing_time=avg_processing_time,
            frame_queue_size=len(self.frame_times)
        )
