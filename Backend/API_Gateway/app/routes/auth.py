from fastapi import APIRouter
from app.services.auth_client import login

router = APIRouter(prefix="/auth")

@router.post("/login")
async def login_user(data: dict):
    return await login(data)
