from fastapi import APIRouter
import requests
from app.config import settings

router = APIRouter()

@router.get("/{email}")
def get_profile(email: str):
    return requests.get(
        f"{settings.USER_PROFILE_URL}/profiles/{email}"
    ).json()
