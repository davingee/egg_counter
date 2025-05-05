import json
from datetime import datetime
import redis
from egg_counter_shared import helper


class RedisManager:
    def __init__(self, settings):
        self.client = redis.Redis.from_url(settings.redis_url, decode_responses=True)
        self.settings = settings
        self.redis_key_checked = {}
        self._initialize_redis_keys()

    def _initialize_redis_keys(self):
        key = helper.get_redis_count_key()
        if key not in self.redis_key_checked:
            if not self.client.exists(key):
                self.client.hset(key, mapping={"house1": 0, "house2": 0})
                self.client.expire(key, helper.seconds_until_midnight())
            self.redis_key_checked[key] = True

    def increment_count(self, house_number):
        key = helper.get_redis_count_key()
        self.client.hincrby(key, f"house{house_number}", 1)
        self._publish_counts()

    def update_conveyor_status(self, status):
        self.client.set("eggs:conveyor_status", status)
        self.client.publish(
            "conveyor-status",
            json.dumps({"status": status, "timestamp": datetime.now().isoformat()}),
        )

    def _publish_counts(self):
        key = helper.get_redis_count_key()
        data = self.client.hgetall(key)
        self.client.publish(
            "house-counts",
            json.dumps(
                {
                    "house1": int(data.get("house1", 0)),
                    "house2": int(data.get("house2", 0)),
                }
            ),
        )
