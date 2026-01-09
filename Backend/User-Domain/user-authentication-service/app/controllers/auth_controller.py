from fastapi import APIRouter, HTTPException, status
from app.schemas.auth_schema import LoginRequest, LoginResponse
from app.services.auth_service import authenticate_user


router = APIRouter()

@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest):
    result = authenticate_user(
        email=request.email,
        password=request.password
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    return result
