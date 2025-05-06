import cv2
import numpy as np


class ImageProcessor:
    def __init__(self, settings):
        self.lower_hsv = np.array(settings.lower_hsv)
        self.upper_hsv = np.array(settings.upper_hsv)
        self.min_area = settings.min_area
        self.max_area = settings.max_area

    def detect_contours(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower_hsv, self.upper_hsv)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return [
            c for c in contours if self.min_area <= cv2.contourArea(c) <= self.max_area
        ]
