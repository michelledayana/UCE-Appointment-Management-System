from fastapi import APIRouter, Body
from app.services.user_service import UserService

router = APIRouter(prefix="/users")

@router.post("/register")
def register_user(data: dict = Body(...)):
    return UserService.register_user(
        data["full_name"],
        data["email"]
    )
