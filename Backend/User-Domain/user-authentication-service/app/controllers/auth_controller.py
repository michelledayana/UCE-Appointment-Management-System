from fastapi import APIRouter, HTTPException
from app.schemas.auth_schema import LoginRequest
from app.services.auth_service import authenticate_user
from app.security.jwt_handler import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/login")
def login(data: LoginRequest):
    user = authenticate_user(data.email, data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "sub": user.email,
        "role": user.user_type
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }