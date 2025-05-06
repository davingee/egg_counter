from datetime import datetime, timedelta
import pytz  # type: ignore
from pydantic import BaseModel  # type: ignore
from pathlib import Path


def time_zone():
    return "America/Denver"


MOUNTAIN_TZ = pytz.timezone(time_zone())

project_root = Path(__file__).resolve().parents[1]


def video_path():
    return f"{project_root}/shared/egg.mp4"


def script_path():
    return f"{project_root}/counter/main.py"


def output_path():
    return f"{project_root}/output/output.avi"


def snapshot_path():
    return f"{project_root}/output/snapshots"


def csv_log_path():
    return f"{project_root}/output/log.csv"


def to_env_name(field_name: str) -> str:
    return field_name.upper()


def utc_time():
    return datetime.now()


def now_time():
    return datetime.now(MOUNTAIN_TZ)


def get_redis_count_key():
    return f"eggs:counts:{now_time().strftime('%Y-%m-%d')}"


def get_redis_house_key() -> str:
    return "eggs:current_house"


def get_redis_app_running_key() -> str:
    return "eggs:running"


def seconds_until_midnight_mtn() -> int:
    now = datetime.now(MOUNTAIN_TZ)
    tomorrow = (now + timedelta(days=1)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    return int((tomorrow - now).total_seconds())


def get_now_minus_days(days):
    end = now_time().date()
    start = end - timedelta(days=days)
    return start, end


def csv_name(date):
    return f"eggs_today_{date}.csv"


class SettingsUpdate(BaseModel):
    debug_logging_enabled: bool
    use_video_file: bool
    webcam_index: int
    webcam_width: int
    webcam_height: int
    show_window: bool
    enable_waitkey: bool
    frame_delay_ms: int
    save_frame_image: bool
    save_video: bool
    csv_log_enabled: bool
    min_area: int
    max_area: int
    y_start_line: int
    y_count_line: int
    num_rows: int
    skip_radius_y: int
    min_frames_between_counts: int
    # lower_hsv: List[int]
    # upper_hsv: List[int]
    rotate_frame: bool
    motion_enabled: bool
    motion_threshold: float
    min_movement_frames: int
    max_stationary_frames: int
    motion_check_interval: int
    email_password: str


class StartRequest(BaseModel):
    house_number: int
    config: SettingsUpdate
