from fastapi import APIRouter, HTTPException
from app.services.user_service_client import register_user

router = APIRouter()

@router.post("/register")
def register(payload: dict):
    response = register_user(payload)
    return response
