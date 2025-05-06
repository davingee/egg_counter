
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from counter.app.counting import RowTracker

def test_should_count_prevents_duplicate_within_radius_and_frame_gap():
    tracker = RowTracker(frame_gap=5, y_radius=10)
    tracker.history.append((1, 100))
    assert not tracker.should_count(3, 105)[0]  # Too close in time and position
    assert tracker.should_count(10, 150)[0]     # Far enough in both
