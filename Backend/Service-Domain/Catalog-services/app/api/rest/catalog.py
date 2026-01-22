from fastapi import APIRouter
from app.application.handlers.query_handlers import handle_get_services

router = APIRouter(
    prefix="/catalog",
    tags=["Catalog"]
)

@router.get("/services")
def get_services():
    return handle_get_services()
