from fastapi import Header, HTTPException
from app.security.jwt_handler import decode_token

def admin_required(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)

    if not payload or payload.get("role") != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin only")

    return payload
