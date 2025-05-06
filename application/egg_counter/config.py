from pydantic_settings import BaseSettings, SettingsConfigDict  # type: ignore
from pathlib import Path
from typing import Optional, Tuple
import sys
import os

# project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
# sys.path.insert(0, project_root)
from shared import helper


class Settings(BaseSettings):

    # --------------------------
    # Redis Configuration
    # --------------------------
    redis_url: str = None  # Redis server URL (redis://<host>:<port>)
    # app_path: str = None
    lower_hsv: Tuple[int, int, int] = (0, 0, 100)  # Lower HSV threshold
    upper_hsv: Tuple[int, int, int] = (180, 45, 255)  # Upper HSV threshold
    # debug_logging_enabled: bool = None
    # # --------------------------
    # # Video Input Configuration
    # # --------------------------
    # use_video_file: bool = None  # True=file, False=webcam
    # # video_path: Path = None  # Path to video file when use_video_file=True
    # webcam_index: int = None  # Camera index (default 0)
    # webcam_width: int = None  # Capture width
    # webcam_height: int = None  # Capture height

    # # --------------------------
    # # Display & UI Configuration
    # # --------------------------
    # show_window: bool = None  # Show processing window
    # enable_waitkey: bool = None  # Enable keyboard interrupts
    # frame_delay_ms: int = None  # Delay between frames (ms)

    # # --------------------------
    # # Output Configuration
    # # --------------------------
    # save_frame_image: bool = None  # Save individual frames
    # save_video: bool = None  # Save processed video
    # output_path: Path = None  # Output video path
    # csv_log_enabled: bool = None  # Enable CSV logging
    # csv_log_path: Path = None  # CSV log path
    # snapshots_dir: Path = Path("snapshots")  # Frame images directory

    # # --------------------------
    # # Detection Parameters
    # # --------------------------
    # min_area: int = None  # Minimum contour area (px²)
    # max_area: int = None  # Maximum contour area (px²)
    # y_start_line: int = None  # Detection start Y-coordinate
    # y_count_line: int = None  # Counting line Y-coordinate
    # num_rows: int = None  # Number of tracking rows
    # skip_radius_y: int = None  # Vertical duplicate prevention radius
    # min_frames_between_counts: int = None  # Min frames between row counts

    # # --------------------------
    # # Image Processing
    # # --------------------------
    # rotate_frame: bool = False  # Rotate video 180 degrees

    # # --------------------------
    # # Motion Detection
    # # (Added feature with original null-safe defaults)
    # # --------------------------
    # motion_enabled: bool = None  # Enable/disable motion detection
    # motion_threshold: float = None  # Pixel movement threshold
    # min_movement_frames: int = None  # Smoothing window size
    # max_stationary_frames: int = None  # Frames to declare stopped
    # motion_check_interval: int = None  # Check every N frames

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        alias_generator=helper.to_env_name,
        populate_by_name=True,
    )
