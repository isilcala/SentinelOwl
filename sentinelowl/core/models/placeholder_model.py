import random
import numpy as np
from sentinelowl.core.models.base_model import BaseModel


class PlaceholderModel(BaseModel):
    def __init__(self, warning_threshold=0.7, critical_threshold=0.85):
        self.warning_threshold = warning_threshold
        self.critical_threshold = critical_threshold

    def predict(self, frame: np.ndarray) -> tuple[float, bool, bool]:
        confidence = random.random()
        return (
            confidence,
            confidence > self.warning_threshold,
            confidence > self.critical_threshold,
        )
