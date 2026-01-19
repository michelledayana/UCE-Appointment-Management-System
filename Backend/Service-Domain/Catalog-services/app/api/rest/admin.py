from fastapi import APIRouter, status
from app.schemas.service_schema import ServiceCreate, ServiceUpdate
from app.application.commands.create_service import create_service_command
from app.application.commands.update_service import update_service_command
from app.application.commands.disable_service import disable_service_command

router = APIRouter(
    prefix="/admin/catalog",
    tags=["Admin Catalog"]
)

@router.post(
    "/services",
    status_code=status.HTTP_201_CREATED
)
def create_service(service: ServiceCreate):
    return create_service_command(service)

@router.put("/services/{service_id}")
def update_service(service_id: str, service: ServiceUpdate):
    return update_service_command(service_id, service)

@router.delete("/services/{service_id}")
def disable_service(service_id: str):
    return disable_service_command(service_id)
