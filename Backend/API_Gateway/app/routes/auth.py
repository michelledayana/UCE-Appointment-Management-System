from fastapi import APIRouter
import requests
from app.config import settings

router = APIRouter()

@router.post("/login")
def login(payload: dict):
    return requests.post(
        f"{settings.AUTH_SERVICE_URL}/auth/login",
        json=payload
    ).json()
