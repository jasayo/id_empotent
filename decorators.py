from functools import wraps
from .redis import redis_client
import json


def idempotent():
    """
    Decorator that enforces request's Idempotence.
    Saves first request hash in consecutive attempts
    to reach endpoint and its response to redis-storage.
    Next requests receive same result.
    """

    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            key = request.META.get()
            if redis_client.exists(key):
                response = json.loads(
                    redis_client.get(key))
                return response
            response = func(request, *args, **kwargs)
            redis_client.set_temp(key,
                                  json.dumps(response.data),
                                  60 * 60)
            return response

        return inner

    return decorator