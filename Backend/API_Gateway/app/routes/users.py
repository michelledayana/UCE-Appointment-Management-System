from fastapi import APIRouter
import requests
from app.config import settings

router = APIRouter()

@router.post("/register")
def register_user(data: dict):
    return requests.post(
        f"{settings.USER_REGISTRATION_URL}/users/register",
        json=data
    ).json()

@router.post("/login")
def login(data: dict):
    return requests.post(
        f"{settings.AUTH_SERVICE_URL}/auth/login",
        json=data
    ).json()
