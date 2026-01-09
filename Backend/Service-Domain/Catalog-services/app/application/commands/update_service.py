from app.infrastructure.db.mongo import services_collection
from app.schemas.service_schema import ServiceUpdate
from bson import ObjectId

def update_service_command(service_id: str, service: ServiceUpdate):
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
        {"_id": ObjectId(service_id)},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise ValueError("Service not found")

    return {
        "id": service_id,
        "message": "Service updated successfully"
    }
