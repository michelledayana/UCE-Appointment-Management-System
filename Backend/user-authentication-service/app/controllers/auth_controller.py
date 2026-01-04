from fastapi import APIRouter
from app.schemas.auth_schema import LoginRequest
from app.services.auth_service import authenticate

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
def login(data: LoginRequest):
    return authenticate(data.email, data.password)
