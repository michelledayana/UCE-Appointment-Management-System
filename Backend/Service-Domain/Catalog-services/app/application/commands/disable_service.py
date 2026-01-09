from app.infrastructure.db.mongo import services_collection

def disable_service_command(service_id: str):
    result = services_collection.find_one_and_update(
        {"_id": service_id},
        {"$set": {"is_active": False}},
        return_document=True
    )

    if not result:
        raise ValueError("Service not found")

    return result
