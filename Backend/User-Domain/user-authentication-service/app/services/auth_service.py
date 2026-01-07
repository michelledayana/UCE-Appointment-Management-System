from app.database.db import SessionLocal
from app.models.auth_model import AuthUser
from app.security.password import verify_password
from app.security.jwt_handler import create_access_token

def authenticate_user(email: str, password: str):
    db = SessionLocal()
    # BUSCAMOS EN NUESTRA DB LOCAL (auth_db)
    user = db.query(AuthUser).filter(AuthUser.email == email).first()
    db.close()

    if not user or not verify_password(password, user.password_hash):
        return None

    # El token llevará el email y el rol del usuario
    token = create_access_token({
        "sub": user.email,
        "role": user.user_type
    })

    return {"access_token": token, "token_type": "bearer"}
    if not verify_password(password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token = create_access_token({
        "sub": user["email"],
        "role": user["user_type"]
    })

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
