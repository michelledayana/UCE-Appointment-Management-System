from fastapi import Request, HTTPException
from app.security.jwt_handler import decode_token

PUBLIC_ROUTES = [
    "/auth/login",
    "/users/register",
    "/health",
    "/docs",
    "/openapi.json",
    "/redoc",
]

async def auth_middleware(request: Request, call_next):
    # Permitir rutas públicas
    if request.url.path in PUBLIC_ROUTES:
        return await call_next(request)
    
    # Verificar token en rutas protegidas
    auth_header = request.headers.get("Authorization")
    
    if not auth_header:
        raise HTTPException(
            status_code=401, 
            detail="Missing Authorization header"
        )
    
    try:
        # Extraer token
        token = auth_header.replace("Bearer ", "")
        
        # Decodificar y validar
        payload = decode_token(token)
        
        if not payload:
            raise HTTPException(
                status_code=401, 
                detail="Invalid token"
            )
        
        # Agregar user al request state
        request.state.user = payload
        
    except Exception as e:
        raise HTTPException(
            status_code=401, 
            detail=f"Authentication failed: {str(e)}"
        )
    
    return await call_next(request)