import redis
from app.config import REDIS_HOST, REDIS_PORT, REDIS_DB

# Cliente Redis
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True
)

def get_availability(service_id: str):
    """
    Obtiene disponibilidad del cache Redis
    """
    value = redis_client.get(f"availability:{service_id}")
    if value is not None:
        return value == "True"
    return None

def set_availability(service_id: str, value: bool):
    """
    Guarda disponibilidad en Redis
    """
    redis_client.set(f"availability:{service_id}", str(value))
