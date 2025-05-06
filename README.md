# Egg Counter Web App

A real‑time egg‑counting dashboard built with **FastAPI**, **Redis**, **PostgreSQL**, **Alpine.js**, and **Chart.js**, plus a shared helper library. It tracks two “houses” of eggs, streams live counts over WebSockets, persists daily totals, and lets you manage settings and export reports.

---

## 🚀 Features

- **Real‑time updates** via Redis Pub/Sub & WebSockets
- **Fallback to PostgreSQL** if Redis data is missing
- **Start/Stop** counter subprocess per house
- **Select active house** on the fly
- **Daily persistence**: upsert into `eggs` table with date
- **Trends chart** showing counts over the last N days
- **Settings UI** (video, detection, output, etc.) saved in Postgres
- **Export & email** CSV reports for any date
- **Modular code** split into logical packages
- **Shared helper** code kept in a sibling `egg_counter_shared` package

---

## 📦 Repository Structure

\`\`\`text
egg_counter_web/
├─ main.py                    ← App entry point, mounts static & templates, includes routes & websocket
├─ .env                       ← Environment variables (DB, Redis, etc.)
├─ requirements.txt           ← Python dependencies
├─ static/                    ← CSS, JS, images
├─ templates/                 ← Jinja2 HTML templates
└─ egg_counter/               ← Core application logic
   ├─ config.py               ← Pydantic settings & env loading
   ├─ clients.py              ← Redis & Postgres client initialization
   ├─ counts.py               ← Redis fetch, fallback, upsert functions
   ├─ controller.py           ← Subprocess manager for egg-counter script
   ├─ schemas.py              ← Pydantic models for request bodies
   ├─ helper.py               ← Local helper wrappers (moved / overridden by shared)
   ├─ api/
   │  ├─ routes.py            ← All REST endpoints (status, counts, start/stop, settings, trends)
   │  └─ websocket.py         ← WebSocket endpoint for live counts
   └─ services/
      ├─ upsert.py            ← Database upsert logic
      └─ csv_export.py        ← CSV export & email logic

egg_counter_shared/
└─ helper.py                  ← Utility functions (e.g. key generators, date math)
\`\`\`

---

## ⚙️ Prerequisites

1. **Python 3.10+**
2. **PostgreSQL** database with an `eggs` table:
   \`\`\`sql
   CREATE TABLE eggs (
     id            SERIAL PRIMARY KEY,
     house_number  INTEGER NOT NULL,
     date          DATE NOT NULL,
     count         INTEGER NOT NULL,
     created_at    TIMESTAMP DEFAULT NOW(),
     updated_at    TIMESTAMP DEFAULT NOW(),
     UNIQUE (house_number, date)
   );
   \`\`\`
3. **Redis** instance (>= 6.x) for pub/sub and caching.
4. **.env** file in \`egg_counter_web/\`:
   \`\`\`ini
   PG_DB=your_db_name
   PG_USER=your_user
   PG_HOST=localhost
   PG_PORT=5432
   PG_PASS=your_password
   REDIS_URL=redis://localhost:6379
   \`\`\`
5. **egg_counter_shared/** installed as an editable package (see Installation).

---

## 🛠️ Installation

\`\`\`bash
# Clone both repos under the same parent folder:
git clone git@github.com:you/egg_counter_shared.git
git clone git@github.com:you/egg_counter_web.git

# Install shared helper in editable mode:
cd egg_counter_shared
pip install -e .

# Install web app requirements:
cd ../egg_counter_web
pip install -r requirements.txt
\`\`\`

---

## 🔧 Configuration

- Edit \`.env\` with your DB/Redis credentials.
- Ensure \`egg_counter_shared/helper.py\` is on your \`PYTHONPATH\`:

  \`\`\`bash
  export PYTHONPATH="../egg_counter_shared:$PYTHONPATH"
  \`\`\`

---

## 🚀 Running Locally

\`\`\`bash
cd egg_counter_web
uvicorn main:app --reload
\`\`\`

- **REST API**:  \`http://localhost:8000/\`
- **WebSocket**: \`ws://localhost:8000/ws/house_counts\`
- **Static files** under \`/static\`
- **Templates** served from \`/templates/index.html\`

---

## 📑 API Endpoints

- \`GET  /status\`
- \`GET  /current_house\`
- \`GET  /current_counts\`
- \`POST /start\`
- \`POST /stop\`
- \`POST /select_house\`
- \`GET  /trends?days=8\`

### Settings

- \`POST /settings/delete_all\`
- \`POST /settings/delete_date\`
- \`POST /settings/clear_redis\`
- \`GET  /settings/get\`
- \`PUT  /settings/update\`
- \`POST /settings/export_csv\`

---

## 🔄 Live Updates

The frontend connects to\`ws://…/ws/house_counts\` and listens for JSON messages:

\`\`\`json
{"house1": 120, "house2": 95}
\`\`\`

It falls back to HTTP polling if the socket fails.

---

## 📝 Contributing

1. Fork the repo
2. Create a feature branch
3. Make your changes, add tests
4. Submit a pull request

---

## 🛡️ License

MIT © Your Name
