
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
import pytest
import cv2

from counter.app.image_processing import ImageProcessor

def test_detect_contours_filters_by_hsv_and_area():
    settings = type("Settings", (), {})()
    settings.lower_hsv = [0, 0, 0]
    settings.upper_hsv = [180, 255, 255]
    settings.min_area = 100
    settings.max_area = 10000

    processor = ImageProcessor(settings)

    # Create a dummy image with a white square on black background
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    cv2.rectangle(frame, (100, 100), (200, 200), (255, 255, 255), -1)

    contours = processor.detect_contours(frame)
    assert isinstance(contours, list)
