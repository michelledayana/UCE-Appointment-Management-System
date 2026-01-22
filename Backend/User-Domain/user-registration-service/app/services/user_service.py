from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import logging

from app.models.user_model import User
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password
from app.messaging.kafka_producer import publish_user_registered_event


class UserService:

    @staticmethod
    def register_user(db: Session, full_name: str, email: str, password: str):

        # Verificar si el email ya está registrado
        if UserRepository.get_by_email(db, email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Definir tipo de usuario
        user_type = "STUDENT" if email.endswith("@uce.edu.ec") else "GENERAL"

        # Crear el usuario
        new_user = User(
            full_name=full_name,
            email=email,
            password_hash=hash_password(password),
            user_type=user_type
        )

        # Guardar en la base de datos
        UserRepository.save(db, new_user)
        db.refresh(new_user)

        # Publicar evento Kafka, pero manejar fallos
        try:
            publish_user_registered_event({
                "id": new_user.id,
                "email": new_user.email,
                "full_name": new_user.full_name,
                "password_hash": new_user.password_hash,
                "user_type": new_user.user_type
            })
        except Exception as e:
            logging.warning(f"Kafka event could not be published: {e}")

        # Retornar la información del usuario
        return {
            "id": new_user.id,
            "email": new_user.email,
            "full_name": new_user.full_name,
            "user_type": new_user.user_type
        }
