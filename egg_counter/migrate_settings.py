import os
import psycopg2
from dotenv import load_dotenv

load_dotenv(override=True)


def main():
    conn = psycopg2.connect(
        dbname=os.getenv("PG_DB"),
        user=os.getenv("PG_USER"),
        host=os.getenv("PG_HOST"),
        port=os.getenv("PG_PORT"),
    )
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS eggs (
            id SERIAL PRIMARY KEY,
            house_number INTEGER NOT NULL,
            count INTEGER NOT NULL,
            date DATE NOT NULL,
            created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );"""
    )

    cur.execute(
        """CREATE TABLE IF NOT EXISTS settings (
          id SERIAL PRIMARY KEY,
          debug_logging_enabled BOOLEAN NOT NULL DEFAULT FALSE,
          use_video_file BOOLEAN NOT NULL DEFAULT FALSE,
          webcam_index INTEGER NOT NULL DEFAULT 0,
          webcam_width INTEGER NOT NULL DEFAULT 640,
          webcam_height INTEGER NOT NULL DEFAULT 480,
          show_window BOOLEAN NOT NULL DEFAULT TRUE,
          enable_waitkey BOOLEAN NOT NULL DEFAULT TRUE,
          frame_delay_ms INTEGER NOT NULL DEFAULT 100,
          save_frame_image BOOLEAN NOT NULL DEFAULT FALSE,
          save_video BOOLEAN NOT NULL DEFAULT FALSE,
          csv_log_enabled BOOLEAN NOT NULL DEFAULT FALSE,
          min_area INTEGER NOT NULL DEFAULT 0,
          max_area INTEGER NOT NULL DEFAULT 0,
          y_start_line INTEGER NOT NULL DEFAULT 150,
          y_count_line INTEGER NOT NULL DEFAULT 200,
          num_rows INTEGER NOT NULL DEFAULT 6,
          skip_radius_y INTEGER NOT NULL DEFAULT 25,
          min_frames_between_counts INTEGER NOT NULL DEFAULT 22,
          rotate_frame BOOLEAN NOT NULL DEFAULT FALSE,
          motion_enabled BOOLEAN NOT NULL DEFAULT TRUE,
          motion_threshold DOUBLE PRECISION NOT NULL DEFAULT 15.0,
          min_movement_frames INTEGER NOT NULL DEFAULT 5,
          max_stationary_frames INTEGER NOT NULL DEFAULT 30,
          motion_check_interval INTEGER NOT NULL DEFAULT 1,
          email_password VARCHAR(255) NOT NULL DEFAULT '',
          created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
          updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
      );"""
    )
    cur.execute(
        """INSERT INTO settings (
    debug_logging_enabled,
    use_video_file,
    webcam_index,
    webcam_width,
    webcam_height,
    show_window,
    enable_waitkey,
    frame_delay_ms,
    save_frame_image,
    save_video,
    csv_log_enabled,
    min_area,
    max_area,
    y_start_line,
    y_count_line,
    num_rows,
    skip_radius_y,
    min_frames_between_counts,
    rotate_frame,
    motion_enabled,
    motion_threshold,
    min_movement_frames,
    max_stationary_frames,
    motion_check_interval,
    email_password
    )
    SELECT
    FALSE, FALSE, 0, 640, 480, TRUE, TRUE, 100,
    FALSE, FALSE, FALSE, 0, 0, 150, 200, 6,
    25, 22, ARRAY[0,0,100], ARRAY[180,45,255], FALSE,
    TRUE, 15.0, 5, 30, 1, ''
    WHERE NOT EXISTS (SELECT 1 FROM settings);
    """
    )
    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
