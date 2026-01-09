from uuid import uuid4
from app.schemas.service_schema import ServiceCreate
from app.infrastructure.db.mongo import services_collection

def handle_create_service(service: ServiceCreate):
    service_doc = {
        "_id": str(uuid4()),
        "name": service.name,
        "description": service.description,
        "is_active": True,
        "prices": {
            "STUDENT": service.student_price,
            "GENERAL": service.general_price
        }
    }

    services_collection.insert_one(service_doc)

    return {
        "id": service_doc["_id"],
        "name": service_doc["name"],
        "description": service_doc["description"],
        "is_active": service_doc["is_active"],
        "prices": service_doc["prices"]
    }
