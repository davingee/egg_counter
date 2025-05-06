import cv2
import os


class Visualizer:
    def __init__(self, settings):
        self.settings = settings
        self.writer = None

    def initialize_display(self):
        if self.settings.show_window:
            cv2.namedWindow("Output", cv2.WINDOW_NORMAL)

    def draw_guides(self, frame, width):
        cv2.line(
            frame,
            (0, self.settings.y_start_line),
            (width, self.settings.y_start_line),
            (0, 255, 0),
            2,
        )
        cv2.line(
            frame,
            (0, self.settings.y_count_line),
            (width, self.settings.y_count_line),
            (0, 0, 255),
            2,
        )

    def draw_contour_marker(self, frame, center, counted):
        color = (255, 0, 255) if counted else (255, 0, 0)
        cv2.circle(frame, center, 8, color, -1)
        cv2.circle(frame, center, 16, (0, 255, 255), 2)

    def draw_status(self, frame, status):
        color_map = {
            "moving": (0, 255, 0),
            "stopped": (0, 0, 255),
            "unknown": (255, 255, 0),
        }
        color = color_map.get(status, (255, 255, 255))
        text = f"Conveyor: {status.upper()}"
        cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    def show_frame(self, frame):
        if self.settings.show_window:
            cv2.imshow("Output", frame)

    def handle_output(self, frame, frame_num, frame_size):
        if self.settings.save_video:
            if self.writer is None:
                fps = (
                    30 / self.settings.frame_delay_ms
                    if self.settings.frame_delay_ms > 0
                    else 30
                )
                fourcc = cv2.VideoWriter_fourcc(*"XVID")
                self.writer = cv2.VideoWriter(
                    str(self.settings.output_path), fourcc, fps, frame_size
                )
            self.writer.write(frame)
        if self.settings.save_frame_image:
            os.makedirs(self.settings.snapshots_dir, exist_ok=True)
            cv2.imwrite(
                f"{self.settings.snapshots_dir}/frame_{frame_num:05d}.jpg", frame
            )

    def cleanup(self):
        if self.writer:
            self.writer.release()
        if self.settings.show_window:
            cv2.destroyAllWindows()
