from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash
from fastapi import HTTPException, status
from app.models.user_model import User
from app.repositories.user_repository import UserRepository

class UserService:

    @staticmethod
    def register_user(
        db: Session,
        full_name: str,
        email: str,
        password: str
    ):
        try:
            # 🔐 Check duplicate email
            existing_user = UserRepository.get_by_email(db, email)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )

            user_type = "STUDENT" if email.endswith("@uce.edu.ec") else "GENERAL"
            password_hash = generate_password_hash(password)

            user = User(
                full_name=full_name,
                email=email,
                password_hash=password_hash,
                user_type=user_type
            )

            UserRepository.save(db, user)

            return {
                "message": "User registered successfully",
                "user_type": user_type
            }

        except HTTPException:
            raise

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
