from app.cache.redis_client import get_availability
import logging

logger = logging.getLogger(__name__)

def validate_availability(service_id: str) -> bool:
    """
    Validates availability using Redis cache
    """
    availability = get_availability(service_id)

    if availability is None:
        logger.warning(f"⚠️ No availability data for service: {service_id}")
        return False

    logger.info(f"✅ Availability for {service_id}: {availability}")
    return availability
