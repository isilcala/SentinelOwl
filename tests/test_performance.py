import time
from sentinelowl.core.performance import PerformanceMonitor, PerformanceStats


def test_performance_monitor():
    """Test performance monitoring"""
    monitor = PerformanceMonitor(window_size=3)

    # 记录第一帧
    monitor.start_frame()
    time.sleep(0.1)  # 模拟处理时间
    monitor.end_frame()

    # 记录第二帧
    monitor.start_frame()
    time.sleep(0.1)
    monitor.end_frame()

    stats = monitor.get_stats()
    assert stats.fps > 0.0  # 现在应该大于0
    assert stats.processing_time > 0.0
