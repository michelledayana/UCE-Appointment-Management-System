import redis
from app.config import REDIS_HOST, REDIS_PORT

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)

def get_availability(service_id: str):
    return redis_client.get(f"availability:{service_id}")

def set_availability(service_id: str, value: bool):
    redis_client.set(f"availability:{service_id}", str(value))
