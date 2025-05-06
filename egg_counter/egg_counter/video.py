import cv2


class VideoCapture:
    def __init__(self, settings):
        self.settings = settings
        self.cap = self._initialize_capture()
        self._frame_size = (
            int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        )
        self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30.0

    def _initialize_capture(self):
        source = (
            str(self.settings.video_path)
            if self.settings.use_video_file
            else self.settings.webcam_index
        )
        cap = cv2.VideoCapture(source)
        if not cap.isOpened():
            raise RuntimeError(f"Failed to open video source: {source}")
        if not self.settings.use_video_file:
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.settings.webcam_width)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.settings.webcam_height)
        return cap

    def read_frame(self):
        success, frame = self.cap.read()
        if success and self.settings.rotate_frame:
            frame = cv2.rotate(frame, cv2.ROTATE_180)
        return success, frame

    def release(self):
        self.cap.release()

    @property
    def frame_size(self):
        return self._frame_size
