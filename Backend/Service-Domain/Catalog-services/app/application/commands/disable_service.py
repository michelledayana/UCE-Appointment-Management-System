from app.infrastructure.db.mongo import services_collection
from app.infrastructure.kafka.producer import publish_service_event
from app.infrastructure.redis.cache import clear_services_cache
from bson import ObjectId

def disable_service_command(service_id: str):
    result = services_collection.update_one(
        {"_id": ObjectId(service_id)},
        {"$set": {"is_active": False}}
    )

    if result.matched_count == 0:
        raise ValueError("Service not found")

    publish_service_event("SERVICE_DISABLED", {
        "id": service_id
    })
    
    clear_services_cache()
   
    return {
        "id": service_id,
        "is_active": False,
        "message": "Service disabled successfully"
    }
