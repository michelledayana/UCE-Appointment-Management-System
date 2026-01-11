from app.infrastructure.db.mongo import services_collection
from app.schemas.service_schema import ServiceUpdate
from app.infrastructure.kafka.producer import publish_service_event
from app.infrastructure.redis.cache import clear_services_cache
from bson import ObjectId
from bson.errors import InvalidId
import logging

logger = logging.getLogger(__name__)

def update_service_command(service_id: str, service: ServiceUpdate):
    try:
        object_id = ObjectId(service_id)
    except InvalidId:
        raise ValueError("Invalid service ID format")

    update_data = {}

    if service.name is not None:
        update_data["name"] = service.name
    if service.description is not None:
        update_data["description"] = service.description
    if service.student_price is not None:
        update_data["prices.STUDENT"] = service.student_price
    if service.general_price is not None:
        update_data["prices.GENERAL"] = service.general_price
    if service.is_active is not None:
        update_data["is_active"] = service.is_active

    if not update_data:
        return {"message": "Nothing to update"}

    result = services_collection.update_one(
        {"_id": object_id},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise ValueError("Service not found")

    # 🔒 Kafka es eventual
    try:
        publish_service_event(
            "SERVICE_UPDATED",
            {
                "id": service_id,
                "updated_fields": list(update_data.keys())
            }
        )
    except Exception as e:
        logger.error(f"Kafka error on SERVICE_UPDATED: {e}")

    # 🔒 Redis es opcional
    try:
        clear_services_cache()
    except Exception as e:
        logger.error(f"Redis cache clear error: {e}")

    return {
        "id": service_id,
        "message": "Service updated successfully"
    }
