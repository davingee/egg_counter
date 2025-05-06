import sys, os
from pathlib import Path

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)
from egg_counter_shared import helper
import argparse
import json
import logging
import sys
from egg_counter.config import Settings
from egg_counter.egg_counter import EggCounter


def main():
    parser = argparse.ArgumentParser(description="Egg Counting System")
    parser.add_argument("--command", choices=["run"], required=True)
    parser.add_argument("--house_number", type=int, choices=[1, 2], required=True)
    parser.add_argument("--config", type=json.loads)

    try:
        args = parser.parse_args()
        settings = Settings()
        app_path = settings.app_path
        updated_settings = settings.model_copy(
            update={
                "video_path": f"{app_path}/{helper.video_path()}",
                "output_path": f"{app_path}/{helper.output_path()}",
                "csv_log_path": f"{app_path}/{helper.csv_log_path()}",
                "snapshots_dir": f"{app_path}/{Path('snapshots')}",
                "debug_logging_enabled": args.config.get("debug_logging_enabled"),
                "use_video_file": args.config.get("use_video_file"),
                "webcam_index": args.config.get("webcam_index"),
                "webcam_width": args.config.get("webcam_width"),
                "webcam_height": args.config.get("webcam_height"),
                "show_window": args.config.get("show_window"),
                "enable_waitkey": args.config.get("enable_waitkey"),
                "frame_delay_ms": args.config.get("frame_delay_ms"),
                "save_frame_image": args.config.get("save_frame_image"),
                "save_video": args.config.get("save_video"),
                "csv_log_enabled": args.config.get("csv_log_enabled"),
                "min_area": args.config.get("min_area"),
                "max_area": args.config.get("max_area"),
                "y_start_line": args.config.get("y_start_line"),
                "y_count_line": args.config.get("y_count_line"),
                "num_rows": args.config.get("num_rows"),
                "skip_radius_y": args.config.get("skip_radius_y"),
                "min_frames_between_counts": args.config.get(
                    "min_frames_between_counts"
                ),
                "rotate_frame": args.config.get("rotate_frame"),
                "motion_enabled": args.config.get("motion_enabled"),
                "motion_threshold": args.config.get("motion_threshold"),
                "min_movement_frames": args.config.get("min_movement_frames"),
                "max_stationary_frames": args.config.get("max_stationary_frames"),
                "motion_check_interval": args.config.get("motion_check_interval"),
            }
        )

        EggCounter(updated_settings, args.house_number).run()
    except Exception:
        logging.exception("Fatal error occurred")
        sys.exit(1)


if __name__ == "__main__":
    main()
