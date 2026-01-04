from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserRegisterRequest
from app.services.user_service import UserService
from app.database.dependencies import get_db

router = APIRouter()

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
