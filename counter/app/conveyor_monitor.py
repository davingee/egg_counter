import numpy as np
import cv2


class ConveyorMonitor:
    def __init__(self, settings):
        self.settings = settings
        self.prev_centroids = []
        self.stationary_frames = 0
        self.movement_history = []
        self.status = "unknown"
        self.frame_counter = 0

    def update(self, contours):
        self.frame_counter += 1
        if (
            not self.settings.motion_enabled
            or self.frame_counter % self.settings.motion_check_interval != 0
        ):
            return self.status

        current_centroids = self._get_centroids(contours)

        if not self.prev_centroids and current_centroids:
            self.prev_centroids = current_centroids
            self.status = "moving"
            return self.status

        if len(current_centroids) != len(self.prev_centroids) or not current_centroids:
            self.prev_centroids = current_centroids
            return self.status

        movement = self._calculate_movement(current_centroids)
        self.movement_history.append(movement)
        if len(self.movement_history) > self.settings.min_movement_frames:
            self.movement_history.pop(0)

        if np.mean(self.movement_history) > self.settings.motion_threshold:
            self.stationary_frames = 0
            self.status = "moving"
        else:
            self.stationary_frames = min(
                self.stationary_frames + 1, self.settings.max_stationary_frames
            )
            if self.stationary_frames >= self.settings.max_stationary_frames:
                self.status = "stopped"

        self.prev_centroids = current_centroids
        return self.status

    def _get_centroids(self, contours):
        return [
            self._contour_centroid(c)
            for c in contours
            if cv2.contourArea(c) >= self.settings.min_area
        ]

    def _contour_centroid(self, contour):
        M = cv2.moments(contour)
        if M["m00"] == 0:
            return (0, 0)
        return (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

    def _calculate_movement(self, current):
        total = sum(
            abs(x2 - x1) + abs(y2 - y1)
            for (x1, y1), (x2, y2) in zip(self.prev_centroids, current)
        )
        return total / len(current)
