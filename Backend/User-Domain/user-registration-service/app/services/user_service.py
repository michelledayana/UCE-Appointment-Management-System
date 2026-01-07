from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user_model import User
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password
from app.messaging.kafka_producer import publish_user_registered_event

class UserService:
    @staticmethod
    def register_user(db: Session, full_name: str, email: str, password: str):
        # Check uniqueness
        if UserRepository.get_by_email(db, email):
            raise HTTPException(status_code=400, detail="Email already registered")

        # UCE Requirement: Automatic classification
        user_type = "STUDENT" if email.endswith("@uce.edu.ec") else "GENERAL"

        new_user = User(
            full_name=full_name,
            email=email,
            password_hash=hash_password(password),
            user_type=user_type
        )
        UserRepository.save(db, new_user)

        # Send data to Kafka for the Auth Service to consume
        event_payload = {
            "user_id": new_user.id,
            "email": new_user.email,
            "password_hash": new_user.password_hash,
            "user_type": new_user.user_type
        }
        publish_user_registered_event(event_payload)

        return {"message": "User registered successfully", "user_type": user_type}