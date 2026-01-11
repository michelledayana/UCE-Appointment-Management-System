from app.schemas.service_schema import ServiceCreate
from app.infrastructure.db.mongo import services_collection
from app.infrastructure.kafka.producer import publish_service_event
from app.infrastructure.redis.cache import clear_services_cache
import logging

logger = logging.getLogger(__name__)

def create_service_command(service: ServiceCreate):
    service_doc = {
        "name": service.name,
        "description": service.description,
        "is_active": True,
        "prices": {
            "STUDENT": service.student_price,
            "GENERAL": service.general_price
        }
    }

    result = services_collection.insert_one(service_doc)
    service_id = str(result.inserted_id)

    event_payload = {
        "id": service_id,
        "name": service.name,
        "prices": service_doc["prices"]
    }

    # 🔒 Kafka NO puede tumbar el servicio
    try:
        publish_service_event("SERVICE_CREATED", event_payload)
    except Exception as e:
        logger.error(f"Kafka error on SERVICE_CREATED: {e}")

    # Redis tampoco debe romper el flujo
    try:
        clear_services_cache()
    except Exception as e:
        logger.error(f"Redis cache clear error: {e}")

    return {
        "id": service_id,
        "name": service.name,
        "description": service.description,
        "is_active": True,
        "prices": service_doc["prices"]
    }
