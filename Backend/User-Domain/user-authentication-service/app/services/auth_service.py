from app.database.db import SessionLocal
from app.models.auth_model import AuthUser
from app.security.password import verify_password


def authenticate_user(email: str, password: str):
    db = SessionLocal()
    try:
        user = db.query(AuthUser).filter(
            AuthUser.email == email
        ).first()

        if not user:
            return None

        if not verify_password(password, user.password_hash):
            return None

        return user
    finally:
        db.close()
