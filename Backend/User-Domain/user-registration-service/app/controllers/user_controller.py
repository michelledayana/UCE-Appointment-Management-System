from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.schemas.user_schema import UserRegisterRequest
from app.services.user_service import UserService
from app.database.dependencies import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(
    request: UserRegisterRequest,
    db: Session = Depends(get_db)
):
    result = UserService.register_user(
        db=db,
        full_name=request.full_name,
        email=request.email,
        password=request.password
    )

    return {
        "status": "success",
        "message": "User registered successfully",
        "data": {
            "id": result["id"],
            "email": result["email"],
            "full_name": result["full_name"],
            "user_type": result["user_type"]
        }
    }
