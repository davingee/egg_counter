import cv2
from collections import deque


class RowTracker:
    def __init__(self, frame_gap, y_radius):
        self.frame_gap = frame_gap
        self.y_radius = y_radius
        self.history = deque(maxlen=frame_gap)

    def should_count(self, frame_num, y):
        for prev_frame, prev_y in self.history:
            if (
                abs(y - prev_y) < self.y_radius
                and (frame_num - prev_frame) < self.frame_gap
            ):
                return (
                    False,
                    f"duplicate (Δy={abs(y - prev_y)}, Δframes={frame_num - prev_frame})",
                )
        self.history.append((frame_num, y))
        return True, "counted"


class CountingManager:
    def __init__(self, settings, redis_manager, house_number):
        self.settings = settings
        self.redis = redis_manager
        self.house_number = house_number
        self.total_count = 0
        self.trackers = [
            RowTracker(settings.min_frames_between_counts, settings.skip_radius_y)
            for _ in range(settings.num_rows)
        ]

    def process_contour(self, contour, frame_width, frame_num, csv_writer=None):
        x, y, w, h = cv2.boundingRect(contour)
        cx, cy = x + w // 2, y + h // 2

        if not (self.settings.y_start_line <= cy <= self.settings.y_count_line):
            return None

        row = min(
            cx * self.settings.num_rows // frame_width, self.settings.num_rows - 1
        )
        should_count, detail = self.trackers[row].should_count(frame_num, cy)

        if should_count:
            self.total_count += 1
            self.redis.increment_count(self.house_number)

        if csv_writer:
            csv_writer.writerow(
                [
                    frame_num,
                    cx,
                    cy,
                    row,
                    "counted" if should_count else "duplicate",
                    detail,
                ]
            )

        return (cx, cy), should_count
