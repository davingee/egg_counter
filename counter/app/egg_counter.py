from .redis_manager import RedisManager
from .video import VideoCapture
from .image_processing import ImageProcessor
from .counting import CountingManager
from .visualizer import Visualizer
from .conveyor_monitor import ConveyorMonitor
from contextlib import contextmanager
import os
from shared import helper
import csv
import cv2


class EggCounter:
    def __init__(self, settings, house_number):
        self.settings = settings
        self.house_number = house_number
        self.frame_num = 0

        self.redis_manager = RedisManager(settings)
        self.video_capture = VideoCapture(settings)
        self.image_processor = ImageProcessor(settings)
        self.counting_manager = CountingManager(
            settings, self.redis_manager, house_number
        )
        self.visualizer = Visualizer(settings)
        self.conveyor_monitor = (
            ConveyorMonitor(settings) if settings.motion_enabled else None
        )
        self.current_status = "unknown"

        self.visualizer.initialize_display()

    def run(self):
        helper.create_pid_file()

        try:

            width, height = self.video_capture.frame_size
            with self._get_csv_writer() as csv_writer:
                while True:
                    success, frame = self.video_capture.read_frame()
                    if not success:
                        break
                    self._process_frame(frame, width, height, csv_writer)
                    if self._should_exit():
                        break
            self._cleanup()
        finally:
            helper.remove_pid_file()

    def _process_frame(self, frame, width, height, csv_writer):
        self.visualizer.draw_guides(frame, width)
        contours = self.image_processor.detect_contours(frame)

        if self.conveyor_monitor:
            self.current_status = self.conveyor_monitor.update(contours)
            self.redis_manager.update_conveyor_status(self.current_status)

        if self.current_status == "stopped":
            self.visualizer.draw_status(frame, self.current_status)
            self.visualizer.show_frame(frame)
            return

        for contour in contours:
            result = self.counting_manager.process_contour(
                contour, width, self.frame_num, csv_writer
            )
            if result:
                center, counted = result
                self.visualizer.draw_contour_marker(frame, center, counted)

        self._update_display(frame, width, height)

    def _update_display(self, frame, width, height):
        self.visualizer.draw_status(frame, self.current_status)
        cv2.putText(
            frame,
            f"Total: {self.counting_manager.total_count}",
            (width - 160, height - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (0, 0, 255),
            2,
        )
        self.visualizer.show_frame(frame)
        self.visualizer.handle_output(
            frame, self.frame_num, self.video_capture.frame_size
        )
        self.frame_num += 1

    def _should_exit(self):
        delay = self.settings.frame_delay_ms if self.settings.frame_delay_ms > 0 else 1
        return (
            self.settings.show_window
            and self.settings.enable_waitkey
            and cv2.waitKey(delay) == 27
        )

    def _cleanup(self):
        self.video_capture.release()
        self.visualizer.cleanup()

    @contextmanager
    def _get_csv_writer(self):
        if not self.settings.csv_log_enabled:
            yield None
            return
        with open(self.settings.csv_log_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["frame", "cx", "cy", "row", "status", "detail"])
            yield writer
