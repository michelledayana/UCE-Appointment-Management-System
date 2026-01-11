from app.store.user_store import users
from app.security.password import verify_password


def authenticate_user(email: str, password: str):
    user_data = users.get(email)

    if not user_data:
        return None

    if not verify_password(password, user_data["password_hash"]):
        return None

    # 🔥 Retornamos una estructura consistente
    return {
        "email": email,
        "user_type": user_data["user_type"]
    }
