import sys, os; sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest
from unittest.mock import MagicMock, patch, ANY

from counter.app.egg_counter import EggCounter


@pytest.fixture
def mock_settings():
    return MagicMock(
        motion_enabled=False,
        rotate_frame='NONE'
    )


@pytest.fixture
def egg_counter(mock_settings):
    with patch("counter.app.egg_counter.RedisManager"), \
         patch("counter.app.egg_counter.VideoCapture") as MockVideoCapture, \
         patch("counter.app.egg_counter.ImageProcessor"), \
         patch("counter.app.egg_counter.CountingManager"), \
         patch("counter.app.egg_counter.Visualizer"), \
         patch("counter.app.egg_counter.ConveyorMonitor"):

        # Mock a dummy video stream with 2 frames: one success, one fail
        mock_capture = MockVideoCapture.return_value
        mock_capture.read_frame.side_effect = [(True, "frame1"), (False, None)]
        mock_capture.frame_size = (640, 480)

        ec = EggCounter(mock_settings, house_number=1)
        ec._process_frame = MagicMock()
        ec._should_exit = MagicMock(return_value=False)
        ec._cleanup = MagicMock()
        return ec


def test_run_calls_process_and_cleanup(egg_counter):
    egg_counter.run()

    # Frame was processed once
    egg_counter._process_frame.assert_called_once_with("frame1", 640, 480, ANY)
    # Cleanup was called
    egg_counter._cleanup.assert_called_once()
