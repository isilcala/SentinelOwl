import numpy as np
from sentinelowl.core.models import PlaceholderModel

def test_placeholder_model():
    """Test the placeholder model"""
    model = PlaceholderModel()
    frame = np.zeros((480, 640, 3), dtype=np.uint8)  # Mock frame
    confidence, is_warning, is_critical = model.predict(frame)

    assert 0.0 <= confidence <= 1.0
    assert isinstance(is_warning, bool)
    assert isinstance(is_critical, bool)