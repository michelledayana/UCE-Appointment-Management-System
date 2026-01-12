from fastapi import APIRouter
import requests
from app.config import settings

router = APIRouter()

@router.get("/health")
def health():
    return requests.get(
        f"{settings.ADMINISTRATION_SERVICE_URL}/admin/health"
    ).json()
