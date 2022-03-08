from django.conf import settings
import redis


class RedisClient:
    client = redis.Redis(host=settings.REDIS_HOST,
                         port=settings.REDIS_PORT)

    def exists(self, key):
        return self.client.exists(key)

    def set(self, key, value):
        self.client.set(key, value)

    def get(self, key):
        return self.client.get(key)

    def set_temp(self, key, value, time):
        self.set(key, value)
        self.client.expire(key, time)


redis_client = RedisClient()