import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from shared import helper
import argparse
import json
import logging
import sys
from app.config import Settings
from app.egg_counter import EggCounter


def main():
    parser = argparse.ArgumentParser(description="Egg Counting System")
    parser.add_argument("--command", choices=["run"], required=True)
    parser.add_argument("--house_number", type=int, choices=[1, 2], required=True)
    parser.add_argument("--config", type=json.loads)

    try:
        args = parser.parse_args()
        settings = Settings()
        updated_settings = settings.model_copy(
            update={
                "video_path": helper.video_path(),
                "output_path": helper.output_path(),
                "csv_log_path": helper.csv_log_path(),
                "snapshots_dir": helper.snapshot_path(),
                "debug_logging_enabled": args.config.get(
                    "debug_logging_enabled", False
                ),
                "use_video_file": args.config.get("use_video_file", True),
                "webcam_index": args.config.get("webcam_index", 0),
                "webcam_width": args.config.get("webcam_width", 640),
                "webcam_height": args.config.get("webcam_height", 480),
                "show_window": args.config.get("show_window", True),
                "enable_waitkey": args.config.get("enable_waitkey", True),
                "frame_delay_ms": args.config.get("frame_delay_ms", 1),
                "save_frame_image": args.config.get("save_frame_image", False),
                "save_video": args.config.get("save_video", True),
                "csv_log_enabled": args.config.get("csv_log_enabled", False),
                "min_area": args.config.get("min_area", 2000),
                "max_area": args.config.get("max_area", 6000),
                "y_start_line": args.config.get("y_start_line", 150),
                "y_count_line": args.config.get("y_count_line", 200),
                "num_rows": args.config.get("num_rows", 6),
                "skip_radius_y": args.config.get("skip_radius_y", 25),
                "min_frames_between_counts": args.config.get(
                    "min_frames_between_counts", 22
                ),
                "rotate_frame": args.config.get("rotate_frame", 'NONE'),
                "motion_enabled": args.config.get("motion_enabled", True),
                "motion_threshold": args.config.get("motion_threshold", 15),
                "min_movement_frames": args.config.get("min_movement_frames", 5),
                "max_stationary_frames": args.config.get("max_stationary_frames", 30),
                "motion_check_interval": args.config.get("motion_check_interval", 1),
            }
        )

        EggCounter(updated_settings, args.house_number).run()
    except Exception:
        logging.exception("Fatal error occurred")
        sys.exit(1)


if __name__ == "__main__":
    main()
