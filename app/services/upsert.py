from app.clients import db
from shared import helper


async def upsert_count(house: int, count: int) -> None:
    query = """
    INSERT INTO eggs (house_number, date, count)
    VALUES (:house, :date, :count)
    ON CONFLICT (house_number, date)
    DO UPDATE SET count = EXCLUDED.count, updated_at = NOW()
    """
    await db.execute(
        query=query,
        values={"house": house, "date": helper.now_time().date(), "count": count},
    )
