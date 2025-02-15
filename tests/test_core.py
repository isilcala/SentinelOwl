# tests/test_core.py
from sentinelowl.core.engine import SentinelOwl
from sentinelowl.config import AppConfig, DetectionConfig
from sentinelowl.core.detector import DefectDetector, DetectionResult

def test_sentinel_owl_initialization():
    """Test SentinelOwl initialization"""
    config = AppConfig()
    owl = SentinelOwl(config)
    assert owl.config.detection.interval == 5

def test_detection_result_handling():
    """Test detection result handling"""
    config = AppConfig()
    owl = SentinelOwl(config)
    
    # Modify: Add missing is_critical parameter
    warning_result = DetectionResult(
        confidence=0.75, 
        is_warning=True,
        is_critical=False  # Explicitly set critical state to False
    )
    owl._handle_result(warning_result)
    
    critical_result = DetectionResult(
        confidence=0.9, 
        is_warning=False,  # Explicitly set warning state
        is_critical=True
    )
    owl._handle_result(critical_result)

def test_detector_initialization():
    """Test detector initialization"""
    config = DetectionConfig(
        warning_threshold=0.65, 
        critical_threshold=0.9
    )
    detector = DefectDetector(config)
    
    # 验证模型参数是否正确传递
    assert detector.model.warning_threshold == 0.65
    assert detector.model.critical_threshold == 0.9

def test_detector_analysis():
    """Test detector analysis"""
    config = DetectionConfig(warning_threshold=0.7, critical_threshold=0.85)
    detector = DefectDetector(config)
    result = detector.analyze(None)  # Pass None as a mock frame
    assert isinstance(result, DetectionResult)
    assert 0.0 <= result.confidence <= 1.0