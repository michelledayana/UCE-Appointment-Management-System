from app.application.commands.create_service import create_service_command
from app.application.commands.update_service import update_service_command
from app.application.commands.disable_service import disable_service_command
from app.schemas.service_schema import ServiceCreate, ServiceUpdate

def handle_create_service(service: ServiceCreate):
    return create_service_command(service)

def handle_update_service(service_id: str, service: ServiceUpdate):
    return update_service_command(service_id, service)

def handle_disable_service(service_id: str):
    return disable_service_command(service_id)
