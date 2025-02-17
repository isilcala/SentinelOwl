import pytest
from sentinelowl.config import CameraConfig
from sentinelowl.core.camera import CameraHandler, CameraConnectionError


def test_camera_reconnect_failure():
    """Test camera reconnection failure handling"""
    config = CameraConfig(url="invalid_url", reconnect_interval=1)
    camera = CameraHandler(config)

    with pytest.raises(CameraConnectionError):
        for _ in range(5):  # 超过最大重试次数
            camera.capture_frame()
