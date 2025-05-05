from typing import Dict
from egg_counter.clients import redis_client, db
from egg_counter_shared import helper


async def get_counts_from_redis() -> Dict[str, int]:
    key = helper.get_redis_count_key()
    counts = await redis_client.hgetall(key)
    return {k: int(v) for k, v in counts.items()}


async def fallback_all_counts() -> dict:
    query = """
        SELECT house_number, count
        FROM eggs
        WHERE date = :date
    """
    rows = await db.fetch_all(query, values={"date": helper.now_time().date()})
    result = {f"house{row['house_number']}": row["count"] for row in rows}
    return {"house1": result.get("house1", 0), "house2": result.get("house2", 0)}


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
