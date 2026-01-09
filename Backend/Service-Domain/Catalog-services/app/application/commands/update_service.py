from app.infrastructure.db.mongo import services_collection
from app.schemas.service_schema import ServiceUpdate

def update_service_command(service_id: str, service: ServiceUpdate):
    update_data = {}

    if service.name is not None:
        update_data["name"] = service.name
    if service.category is not None:
        update_data["category"] = service.category
    if service.description is not None:
        update_data["description"] = service.description
    if service.is_active is not None:
        update_data["is_active"] = service.is_active

    if service.student_price is not None:
        update_data["prices.STUDENT"] = service.student_price
    if service.general_price is not None:
        update_data["prices.GENERAL"] = service.general_price

    result = services_collection.find_one_and_update(
        {"_id": service_id},
        {"$set": update_data},
        return_document=True
    )

    if not result:
        raise ValueError("Service not found")

    return result
