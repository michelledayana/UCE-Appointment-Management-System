from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash
from fastapi import HTTPException, status
from app.database.db import SessionLocal
from app.models.user import User
from app.security.jwt_handler import create_token
from app.messaging.kafka_producer import send_event

def authenticate(email: str, password: str):
    db: Session = SessionLocal()

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )

    if not check_password_hash(user.password, password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )

    token = create_token({
        "user_id": user.id,
        "email": user.email,
        "role": user.user_type
    })

    # Evento Kafka (login exitoso)
    send_event(
        topic="user-authenticated",
        value={
            "user_id": user.id,
            "email": user.email
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
