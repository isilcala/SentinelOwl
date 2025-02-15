from abc import ABC, abstractmethod
import numpy as np


class BaseModel(ABC):
    """Abstract base class for detection models"""

    @abstractmethod
    def predict(self, frame: np.ndarray) -> tuple[float, bool, bool]:
        pass
