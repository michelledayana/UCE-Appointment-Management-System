from fastapi import APIRouter
from app.services.user_client import register

router = APIRouter(prefix="/users")

@router.post("/register")
async def register_user(data: dict):
    return await register(data)
