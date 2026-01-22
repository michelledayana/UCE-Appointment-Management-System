from fastapi import APIRouter, HTTPException, Request
import requests
from app.config import settings

router = APIRouter()

@router.get("/me")
def get_my_profile(request: Request):
    """Obtener perfil del usuario autenticado"""
    try:
        user = request.state.user
        email = user.get("email") or user.get("sub")
        
        response = requests.get(
            f"{settings.USER_PROFILE_URL}/profiles/{email}",
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{email}")
def get_profile(email: str):
    """Obtener perfil por email"""
    try:
        response = requests.get(
            f"{settings.USER_PROFILE_URL}/profiles/{email}",
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/me")
def update_profile(data: dict, request: Request):
    """Actualizar perfil del usuario autenticado"""
    try:
        user = request.state.user
        email = user.get("email") or user.get("sub")
        
        response = requests.put(
            f"{settings.USER_PROFILE_URL}/profiles/{email}",
            json=data,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))