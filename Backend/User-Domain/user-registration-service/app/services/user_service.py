from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user_model import User
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password

class UserService:

    @staticmethod
    def register_user(db: Session, full_name: str, email: str, password: str):
        existing_user = UserRepository.get_by_email(db, email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        user_type = "STUDENT" if email.endswith("@uce.edu.ec") else "GENERAL"

        user = User(
            full_name=full_name,
            email=email,
            password_hash=hash_password(password),
            user_type=user_type
        )

        UserRepository.save(db, user)

        return {
            "message": "User registered successfully",
            "user_type": user_type
        }
