from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.user_schema import UserRegisterRequest
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.database.dependencies import get_db

router = APIRouter()

# 🔹 Register new user
@router.post("/register", status_code=201)
def register_user(
    request: UserRegisterRequest,
    db: Session = Depends(get_db)
):
    return UserService.register_user(
        db=db,
        full_name=request.full_name,
        email=request.email,
        password=request.password
    )

# 🔹 Get user by email (internal / for other services)
@router.get("/by-email/{email}")
def get_user_by_email(
    email: str,
    db: Session = Depends(get_db)
):
    user = UserRepository.get_by_email(db, email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "password_hash": user.password_hash,
        "user_type": user.user_type
    }
