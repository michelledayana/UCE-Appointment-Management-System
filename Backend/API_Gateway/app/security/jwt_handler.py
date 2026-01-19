from jose import jwt, JWTError
from app.config import settings
from typing import Optional, Dict

def decode_token(token: str) -> Optional[Dict]:
    """Decodifica y valida un token JWT"""
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError as e:
        print(f"JWT Error: {e}")
        return None

def verify_token(token: str) -> Dict:
    """Verifica un token y lanza excepción si es inválido"""
    payload = decode_token(token)
    if not payload:
        raise Exception("Invalid token")
    return payload