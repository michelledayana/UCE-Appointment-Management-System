from fastapi import APIRouter
import requests
from app.config import settings

router = APIRouter()

@router.post("/")
def create(data: dict):
    return requests.post(
        f"{settings.APPOINTMENT_CREATION_URL}/appointments",
        json=data
    ).json()

@router.get("/")
def list_all():
    return requests.get(
        f"{settings.APPOINTMENT_MANAGEMENT_URL}/appointments"
    ).json()
