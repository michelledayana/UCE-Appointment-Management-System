from app.schemas.service_schema import ServiceCreate
from app.infrastructure.db.mongo import services_collection

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

    # copiamos el _id de Mongo a un id string
    service_doc["id"] = str(result.inserted_id)

    # eliminamos _id para que FastAPI no falle
    service_doc.pop("_id")

    return service_doc
