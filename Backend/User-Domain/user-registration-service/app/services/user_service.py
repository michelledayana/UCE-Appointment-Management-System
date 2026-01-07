from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user_model import User
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password
from app.messaging.kafka_producer import publish_user_registered_event

class UserService:
    @staticmethod
    def register_user(db: Session, full_name: str, email: str, password: str):
        # 1. Check for duplicates
        if UserRepository.get_by_email(db, email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Registration failed: This email is already registered."
            )

        user_type = "STUDENT" if email.endswith("@uce.edu.ec") else "GENERAL"

        # 2. Save to Database
        new_user = User(
            full_name=full_name,
            email=email,
            password_hash=hash_password(password),
            user_type=user_type
        )
        UserRepository.save(db, new_user)
        db.refresh(new_user)

        # 3. Prepare clean data for response and Kafka
        # This prevents the 500 error by not returning the SQLAlchemy object directly
        user_data_dto = {
            "user_id": str(new_user.id),
            "email": str(new_user.email),
            "full_name": str(new_user.full_name),
            "password_hash": str(new_user.password_hash),
            "user_type": str(new_user.user_type)
        }

        # 4. Resilient Kafka Publication
        try:
            publish_user_registered_event(user_data_dto)
        except Exception as e:
            # If Kafka fails or is slow, we just log it. 
            # The Auth Service will not be affected because the user IS in the DB.
            print(f"Kafka warning (non-blocking): {e}")

        return user_data_dto