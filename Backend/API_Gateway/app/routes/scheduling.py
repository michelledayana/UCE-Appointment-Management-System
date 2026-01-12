from fastapi import APIRouter
import requests
from app.config import settings

router = APIRouter()

@router.post("/")
def create_schedule(data: dict):
    return requests.post(
        f"{settings.SCHEDULING_MANAGEMENT_URL}/schedules",
        json=data
    ).json()

@router.get("/health")
def availability_health():
    return requests.get(
        f"{settings.AVAILABILITY_SERVICE_URL}/health"
    ).json()
