import logging
from app.cache.redis_client import get_availability, set_availability
from app.database.mongo import availability_collection

logger = logging.getLogger(__name__)

def validate_availability(service_id: str) -> bool:
    """
    Valida disponibilidad usando Redis, con fallback a MongoDB
    """
    # 🔹 Intentar Redis
    availability = get_availability(service_id)
    if availability is not None:
        logger.info(f"✅ Availability (cache) for {service_id}: {availability}")
        return availability

    logger.warning(f"⚠️ Cache miss for service: {service_id}")

    # 🔹 Fallback MongoDB
    record = availability_collection.find_one(
        {"service_id": service_id},
        sort=[("created_at", -1)]
    )

    if record:
        availability = record["available"]
        set_availability(service_id, availability)  # actualizar cache
        logger.info(f"📦 Availability loaded from Mongo for {service_id}: {availability}")
        return availability

    logger.error(f"❌ No availability data found for service: {service_id}")
    return False
