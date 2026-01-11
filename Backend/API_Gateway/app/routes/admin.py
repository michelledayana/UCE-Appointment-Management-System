from fastapi import APIRouter
import requests
from app.config import settings

router = APIRouter()

@router.get("/health")
def admin_health():
    return requests.get(
        f"{settings.ADMIN_SERVICE_URL}/admin/health"
    ).json()
