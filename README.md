# Egg Counter & Dashboard

A FastAPI-powered egg counting system with both a web dashboard and a standalone “counter” module.  
Counts eggs in video frames, stores/logs counts in Redis & PostgreSQL, exports CSVs, and streams live updates via WebSockets.

---

## 🔍 Project Overview

1. **Web App** (`main.py` + `/app`)
   - **FastAPI** backend  
   - **Alpine.js + Tailwind CSS** frontend  
   - Real-time egg counts via WebSocket  
   - CSV export & email  
   - Settings management (clear Redis, delete rows, export CSV)

2. **Counter Module** (`/counter`)
   - Pure-Python CLI for video-based egg counting  
   - Reads from webcam or video file  
   - Uses OpenCV for detection & tracking  
   - Optional Redis pub/sub for real-time push  

3. **Shared Utilities** (`/shared`)
   - Helper functions  
   - Migration scripts  

---

## 📦 Prerequisites

- Python 3.9+  
- Redis server (for live count pub/sub)  
- PostgreSQL (for historical logging)  
- Node.js & npm (for asset build)

---

## ⚙️ Installation

1. Clone repo  
   ```bash
   git clone https://github.com/your-org/egg-counter.git
   cd egg-counter
   ```

2. Create virtual environment & install  
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Install JS deps and build  
   ```bash
   cd static
   npm install
   npm run build
   cd ..
   ```

4. Configure environment variables in `.env`  
   ```ini
   REDIS_URL=redis://localhost:6379
   DATABASE_URL=postgresql://user:pass@localhost:5432/eggdb
   EMAIL_HOST=smtp.mail.com
   EMAIL_PASSWORD=yourpassword
   ```

---

## 🗂️ File Structure

```
.
├── main.py                  # entrypoint for FastAPI app
├── app/
│   ├── controller.py        # request handlers
│   ├── config.py            # Pydantic settings
│   ├── schemas.py           # request/response models
│   ├── clients.py           # Redis/Postgres/email clients
│   ├── api/
│   │   ├── websocket.py     # WebSocket manager
│   │   └── routes.py        # HTTP endpoints
│   └── services/
│       ├── csv_export.py    # CSV & email logic
│       └── upsert.py        # DB upsert helper
├── counter/                 # standalone counter module
│   └── app/
│       ├── config.py
│       ├── redis_manager.py
│       ├── counting.py
│       ├── conveyor_monitor.py
│       ├── egg_counter.py
│       ├── image_processing.py
│       ├── video.py
│       └── visualizer.py
│   └── main.py              # CLI launcher
├── shared/
│   ├── helper.py            # shared utilities
│   └── migrate_settings.py  # one-off data migrations
├── static/                  # frontend assets
│   ├── css/
│   └── js/
├── templates/               # Jinja2 HTML templates
│   ├── base.html
│   ├── index.html
│   ├── chart.html
│   ├── options.html
│   ├── settings.html
│   └── navbar.html
├── output/                  # exported CSVs, logs
├── requirements.txt
├── environment.yml
├── .env
└── README.md
```

---

## 🚀 Running the Web App

```bash
# activate venv
uvicorn main:app --reload
```

- **HTTP API** runs on `http://localhost:8000`
- **Web UI** at `http://localhost:8000/`

---

## ⚙️ Counter CLI

```bash
python counter/main.py   --source=webcam       # or --source=video --path=shared/egg.mp4
```

```bash
### ⚙️ Counter CLI (with full `--config` example)

You can override all settings by passing a JSON object to `--config`. For example:
```

```bash
python counter/main.py \
  --command 'run' \
  --house_number 1 \
  --config '{
    "debug_logging_enabled": false,
    "use_video_file": true,
    "webcam_index": 0,
    "webcam_width": 640,
    "webcam_height": 480,
    "show_window": true,
    "enable_waitkey": true,
    "frame_delay_ms": 1,
    "save_frame_image": false,
    "save_video": true,
    "csv_log_enabled": false,
    "min_area": 2000,
    "max_area": 6000,
    "y_start_line": 150,
    "y_count_line": 200,
    "num_rows": 6,
    "skip_radius_y": 25,
    "min_frames_between_counts": 22,
    "rotate_frame": false,
    "motion_enabled": true,
    "motion_threshold": 15,
    "min_movement_frames": 5,
    "max_stationary_frames": 30,
    "motion_check_interval": 1
  }'
```

- Publishes counts to Redis (if configured)  
- Logs to console / CSV  

---

## 🔌 API Endpoints

| Method | Path                       | Description                         |
| ------ | -------------------------- | ----------------------------------- |
| POST   | `/settings/delete_all`     | Delete all count records            |
| POST   | `/settings/delete_date`    | Delete records for a given date     |
| POST   | `/settings/clear_redis`    | Flush all Redis keys                |
| POST   | `/settings/export_csv`     | Generate & email CSV report         |
| GET    | `/counts/today`            | Fetch today’s counts (JSON)         |
| WS     | `/ws/counts`               | Subscribe to live counts via WebSocket |

---

## 🤝 Contributing

1. Fork & branch  
2. Add tests  
3. Submit a PR  

---

## 📄 License

MIT © Your Name / Your Org
