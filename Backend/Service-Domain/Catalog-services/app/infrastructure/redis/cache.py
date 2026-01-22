import json
import redis
from app.config import REDIS_HOST, REDIS_PORT, REDIS_DB

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True
)

SERVICES_CACHE_KEY = "catalog:services"
CACHE_TTL = 60  # segundos

def get_services_cache():
    data = redis_client.get(SERVICES_CACHE_KEY)
    if data:
        return json.loads(data)
    return None

def set_services_cache(services: list):
    redis_client.setex(
        SERVICES_CACHE_KEY,
        CACHE_TTL,
        json.dumps(services)
    )

def clear_services_cache():
    redis_client.delete(SERVICES_CACHE_KEY)
