from fastapi import HTTPException, status
from app.security.password import verify_password
from app.security.jwt_handler import create_access_token
from app.services.user_service_client import get_user_by_email

def authenticate_user(email: str, password: str):
    user = get_user_by_email(email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    if not verify_password(password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token = create_access_token({
        "sub": user["email"],
        "role": user["user_type"]
    })

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
