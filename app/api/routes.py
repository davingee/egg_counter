from fastapi import APIRouter, Request  # type: ignore
from fastapi.responses import FileResponse  # type: ignore
from typing import Dict
from app.clients import redis_client, db
from app.counts import get_counts_from_redis, fallback_all_counts, upsert_count
from app.controller import counter
from app.schemas import HouseSelection, DateSelection, ExportSelection
from app.services.csv_export import (
    send_csv_email,
    export_eggs_to_csv,
    cleanup_egg_csvs,
)
from shared import helper

router = APIRouter()


# @router.get("/", response_class=FileResponse)
# async def read_index():
#     return "static/index.html"


@router.get("/favicon.ico")
def favicon():
    return FileResponse("static/favicon.ico")


@router.get("/status")
async def api_status() -> Dict[str, bool]:
    running = await redis_client.get(helper.get_redis_app_running_key())
    return {"running": running == "1"}


@router.get("/current_house")
async def api_current_house() -> Dict[str, int]:
    val = await redis_client.get(helper.get_redis_house_key())
    return {"house": int(val) if val else 1}


@router.get("/current_counts")
async def api_current_counts() -> Dict[str, int]:
    counts = await get_counts_from_redis()
    if counts.get("house1") is None and counts.get("house2") is None:
        fallback = await fallback_all_counts()
        await redis_client.hset(helper.get_redis_count_key(), mapping=fallback)
        await redis_client.expire(
            helper.get_redis_count_key(), helper.seconds_until_midnight_mtn()
        )
        counts = await get_counts_from_redis()
    return counts


async def start_counter(house_number: int, values):
    counter.start(house_number, values)
    await redis_client.set(helper.get_redis_app_running_key(), "1")


@router.post("/start")
async def api_start(body: helper.StartRequest) -> Dict[str, bool]:
    await start_counter(body.house_number, body.config.model_dump())
    return {"ok": True}


async def stop_and_save(house_number: int):
    counter.stop()
    await redis_client.set(helper.get_redis_app_running_key(), "0")
    counts = await get_counts_from_redis()
    count = counts.get(f"house{house_number}", 0)
    await upsert_count(house_number, count)


@router.post("/stop")
async def api_stop(request: Request) -> Dict[str, bool]:
    data = await request.json()
    await stop_and_save(int(data["house_number"]))
    return {"ok": True}


@router.post("/select_house")
async def api_select_house(body: helper.StartRequest) -> Dict[str, int]:
    key = helper.get_redis_house_key()
    old = int(await redis_client.get(key) or 1)
    running = (await api_status())["running"]
    await redis_client.set(key, body.house_number)
    if running:
        await stop_and_save(old)
        await start_counter(body.house_number, body.config.model_dump())
    return {"house": body.house_number}


@router.get("/trends")
async def api_trends(days: int = 8) -> Dict[str, list]:
    start, end = helper.get_now_minus_days(days)
    query = """
    SELECT date, house_number, count
    FROM eggs
    WHERE date BETWEEN :start AND :end
    ORDER BY date, house_number
    """
    rows = await db.fetch_all(query=query, values={"start": start, "end": end})
    dates = sorted({r["date"].isoformat() for r in rows})
    return {
        "dates": dates,
        "house1": [
            next(
                (
                    r["count"]
                    for r in rows
                    if r["date"].isoformat() == d and r["house_number"] == 1
                ),
                0,
            )
            for d in dates
        ],
        "house2": [
            next(
                (
                    r["count"]
                    for r in rows
                    if r["date"].isoformat() == d and r["house_number"] == 2
                ),
                0,
            )
            for d in dates
        ],
    }


# Settings endpoints
@router.post("/settings/delete_all")
async def api_delete_all_rows():
    deleted = await db.execute("DELETE FROM eggs;")
    return {"deleted": deleted}


@router.post("/settings/delete_date")
async def api_delete_rows_by_date(selection: DateSelection):
    deleted = await db.execute(
        "DELETE FROM eggs WHERE date = :date", values={"date": selection.date}
    )
    return {"deleted": deleted}


@router.post("/settings/clear_redis")
async def api_clear_redis_keys():
    keys = await redis_client.keys("eggs:*")
    deleted = await (redis_client.delete(*keys) if keys else 0)
    return {"deleted_keys": deleted}


@router.get("/settings/get")
async def api_get_settings():
    row = await db.fetch_one("SELECT * FROM settings LIMIT 1")
    return {} if not row else helper.SettingsUpdate(**row)


@router.put("/settings/update")
async def api_update_settings(values: helper.SettingsUpdate):
    data = values.model_dump()
    data["updated_at"] = helper.utc_time()
    await db.execute(
        """
        UPDATE settings SET
          debug_logging_enabled = :debug_logging_enabled,
          use_video_file = :use_video_file,
          webcam_index = :webcam_index,
          webcam_width = :webcam_width,
          webcam_height = :webcam_height,
          show_window = :show_window,
          enable_waitkey = :enable_waitkey,
          frame_delay_ms = :frame_delay_ms,
          save_frame_image = :save_frame_image,
          save_video = :save_video,
          csv_log_enabled = :csv_log_enabled,
          min_area = :min_area,
          max_area = :max_area,
          y_start_line = :y_start_line,
          y_count_line = :y_count_line,
          num_rows = :num_rows,
          skip_radius_y = :skip_radius_y,
          min_frames_between_counts = :min_frames_between_counts,
          rotate_frame = :rotate_frame,
          motion_enabled = :motion_enabled,
          motion_threshold = :motion_threshold,
          min_movement_frames = :min_movement_frames,
          max_stationary_frames = :max_stationary_frames,
          motion_check_interval = :motion_check_interval,
          email_password = :email_password,
          updated_at = :updated_at
        """,
        data,
    )
    return {"status": "ok"}


@router.post("/settings/export_csv")
async def api_export_csv(options: ExportSelection):
    cleanup_egg_csvs()
    csv_path = await export_eggs_to_csv(options.date)
    send_csv_email(
        smtp_server="smtp.gmail.com",
        port=465,
        sender_email="scottsmit@gmail.com",
        sender_password=options.password,
        recipient_email="scottsmit@gmail.com",
        file_path=csv_path,
        content=f"Attached is your CSV report from {options.date} to today.",
    )
    return {"exported_and_emailed_csv": True}
