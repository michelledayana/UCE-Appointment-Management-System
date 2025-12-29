from fastapi import APIRouter
from app.services.user_service import UserService

router = APIRouter()
service = UserService()

@router.post("/users/register")
def register_user(full_name: str, email: str):
    user = service.register_user(full_name, email)
    return {
        "id": str(user.id),
        "email": user.email,
        "is_student": user.is_student
    }
