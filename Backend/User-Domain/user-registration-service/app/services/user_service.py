from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user_model import User
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password
from app.messaging.kafka_producer import publish_user_registered_event


class UserService:

    @staticmethod
    def register_user(db: Session, full_name: str, email: str, password: str):

        if UserRepository.get_by_email(db, email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        user_type = "STUDENT" if email.endswith("@uce.edu.ec") else "GENERAL"

        new_user = User(
            full_name=full_name,
            email=email,
            password_hash=hash_password(password),
            user_type=user_type
        )

        UserRepository.save(db, new_user)
        db.refresh(new_user)

        publish_user_registered_event({
            "id": new_user.id,
            "email": new_user.email,
            "full_name": new_user.full_name,
            "password_hash": new_user.password_hash,
            "user_type": new_user.user_type
        })

        return {
            "id": new_user.id,
            "email": new_user.email,
            "full_name": new_user.full_name,
            "user_type": new_user.user_type
        }
