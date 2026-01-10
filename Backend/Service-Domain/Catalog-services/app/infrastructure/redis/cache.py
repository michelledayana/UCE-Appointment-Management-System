import json
import redis
from app.config import REDIS_HOST, REDIS_PORT

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)

SERVICES_CACHE_KEY = "catalog:services"
CACHE_TTL = 60  # seconds


def get_services_cache():
    """
    Get services list from Redis cache
    """
    data = redis_client.get(SERVICES_CACHE_KEY)
    if data:
        return json.loads(data)
    return None


def set_services_cache(services: list):
    """
    Store services list in Redis cache
    """
    redis_client.setex(
        SERVICES_CACHE_KEY,
        CACHE_TTL,
        json.dumps(services)
    )


def clear_services_cache():
    """
    Clear services cache
    """
    redis_client.delete(SERVICES_CACHE_KEY)
