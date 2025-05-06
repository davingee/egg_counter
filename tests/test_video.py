
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from unittest.mock import MagicMock, patch
import numpy as np
import cv2

from counter.app.video import VideoCapture

@patch("cv2.VideoCapture")
def test_video_capture_initialization(mock_cv2_capture):
    mock_cap = MagicMock()
    mock_cap.get.side_effect = [640, 480, 30.0]
    mock_cv2_capture.return_value = mock_cap

    settings = MagicMock()
    settings.use_video_file = False
    settings.webcam_index = 0

    capture = VideoCapture(settings)
    assert capture.frame_size == (640, 480)
    assert capture.fps == 30.0
