from app.security.jwt_handler import create_access_token
from jose import jwt
from app.config import settings

def test_create_access_token():
    data = {
        "sub": "test@email.com",
        "role": "GENERAL"
    }

    token = create_access_token(data)

    decoded = jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM]
    )

    assert decoded["sub"] == "test@email.com"
    assert decoded["role"] == "GENERAL"
    assert "exp" in decoded
