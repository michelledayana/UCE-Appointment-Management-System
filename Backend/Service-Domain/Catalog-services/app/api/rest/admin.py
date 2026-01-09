from fastapi import APIRouter
from app.schemas.service_schema import ServiceCreate, ServiceUpdate

router = APIRouter(
    prefix="/admin/catalog",
    tags=["Admin Catalog"]
)

@router.post("/services")
def create_service(service: ServiceCreate):
    return {
        "message": "Service created",
        "data": service
    }

@router.put("/services/{service_id}")
def update_service(service_id: str, service: ServiceUpdate):
    return {
        "message": f"Service {service_id} updated",
        "data": service
    }

@router.delete("/services/{service_id}")
def delete_service(service_id: str):
    return {
        "message": f"Service {service_id} deleted"
    }
