from fastapi import Request, HTTPException
from app.security.jwt_handler import verify_token

PUBLIC_ROUTES = [
    "/auth/login",
    "/users/register",
    "/docs",
    "/openapi.json"
]

async def auth_middleware(request: Request, call_next):
    if request.url.path not in PUBLIC_ROUTES:
        auth = request.headers.get("Authorization")
        if not auth:
            raise HTTPException(401, "Missing Authorization header")

        token = auth.split(" ")[1]
        request.state.user = verify_token(token)

    return await call_next(request)
