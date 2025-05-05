import redis.asyncio as aioredis
import redis.asyncio as redis
from databases import Database
from egg_counter.config import settings

redis_client = aioredis.from_url(settings.redis_url, decode_responses=True)
pubsub_redis = redis.Redis()
db = Database(
    f"postgresql://{settings.pg_user}:{settings.pg_pass}@{settings.pg_host}:{settings.pg_port}/{settings.pg_db}"
)
CHANNEL = "house-counts"
