from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.user_schema import UserRegisterRequest
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.database.dependencies import get_db
# IMPORTANTE: Importa tu función de Kafka
from app.utils.kafka_producer import publish_user_registered_event 

router = APIRouter()

# 🔹 Registro de nuevo usuario
# Cambiamos la ruta a "/usuario". Como en el main.py pusiste prefix="/register", 
# el link final será: http://localhost:8081/register/usuario
@router.post("/usuario", status_code=201)
def register_user(
    request: UserRegisterRequest,
    db: Session = Depends(get_db)
):
    # 1. Registramos en la base de datos local (db_registration)
    new_user = UserService.register_user(
        db=db,
        full_name=request.full_name,
        email=request.email,
        password=request.password
    )

    # 2. Preparamos los datos para enviar a Kafka (Microservicio de Autenticación)
    # Enviamos el hash para que el microservicio de Auth pueda validar el login después
    kafka_data = {
        "email": new_user.email,
        "password": new_user.password_hash, # Enviamos el hash, no la clave plana
        "full_name": new_user.full_name,
        "action": "CREATE_USER"
    }

    # 3. PUBLICAR EN KAFKA
    publish_user_registered_event(kafka_data)

    return new_user

# 🔹 Obtener usuario por email
@router.get("/by-email/{email}")
def get_user_by_email(
    email: str,
    db: Session = Depends(get_db)
):
    user = UserRepository.get_by_email(db, email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "password_hash": user.password_hash,
        "user_type": user.user_type
    }