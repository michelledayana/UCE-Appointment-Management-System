from uuid import uuid4
from app.schemas.service_schema import ServiceCreate
from app.infrastructure.db.mongo import services_collection

def create_service_command(service: ServiceCreate):
    service_doc = {
        "_id": str(uuid4()),
        "name": service.name,
        "category": service.category,
        "description": service.description,
        "is_active": True,
        "prices": {
            "STUDENT": float(service.student_price),
            "GENERAL": float(service.general_price)
        }
    }

    services_collection.insert_one(service_doc)

    return {
        "id": service_doc["_id"],
        "name": service_doc["name"],
        "category": service_doc["category"],
        "description": service_doc["description"],
        "is_active": service_doc["is_active"],
        "prices": service_doc["prices"]
    }
