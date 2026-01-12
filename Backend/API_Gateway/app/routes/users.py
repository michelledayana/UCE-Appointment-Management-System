from fastapi import APIRouter
import requests
from app.config import settings

router = APIRouter()

@router.post("/register")
def register(data: dict):
    return requests.post(
        f"{settings.USER_REGISTRATION_URL}/users/register",
        json=data
    ).json()
