from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.database.db import SessionLocal
from app.models.auth_model import AuthUser
from app.security.password import verify_password
from app.security.jwt_handler import create_access_token



def authenticate_user(email: str, password: str):
    db = SessionLocal()

    try:
        # Buscar usuario en auth DB
        user = db.query(AuthUser).filter(AuthUser.email == email).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        # Verificar contraseña (pbkdf2_sha256)
        if not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        # Crear JWT con email y rol
        access_token = create_access_token({
            "sub": user.email,
            "role": user.user_type
        })

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    finally:
        db.close()
