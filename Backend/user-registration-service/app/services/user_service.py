from app.models.user_model import User
from app.repositories.user_repository import UserRepository
from app.config import SessionLocal

class UserService:

    @staticmethod
    def register_user(full_name: str, email: str):
        db = SessionLocal()

        try:
            # Regla de negocio
            user_type = "STUDENT" if email.endswith("@uce.edu.ec") else "GENERAL"

            # Crear entidad
            user = User(
                full_name=full_name,
                email=email,
                user_type=user_type
            )

            # Guardar en BD
            UserRepository.save(db, user)

            return {
                "message": "User registered successfully",
                "user_type": user_type,
                "email": email
            }

        except Exception as e:
            db.rollback()
            raise e

        finally:
            db.close()
