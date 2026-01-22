from fastapi import APIRouter, Depends, HTTPException
import requests
from app.config import settings
from app.security.dependencies import admin_required

router = APIRouter()

@router.get("/services")
def list_services():
    """Listar todos los servicios"""
    try:
        response = requests.get(
            f"{settings.SERVICE_CATALOG_URL}/catalog/services",
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/services/{service_id}")
def get_service(service_id: str):
    """Obtener servicio por ID"""
    try:
        response = requests.get(
            f"{settings.SERVICE_CATALOG_URL}/catalog/services/{service_id}",
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/services", dependencies=[Depends(admin_required)])
def create_service(data: dict):
    """Crear nuevo servicio (Solo Admin)"""
    try:
        response = requests.post(
            f"{settings.SERVICE_CATALOG_URL}/admin/catalog/services",
            json=data,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/services/{service_id}", dependencies=[Depends(admin_required)])
def update_service(service_id: str, data: dict):
    """Actualizar servicio (Solo Admin)"""
    try:
        response = requests.put(
            f"{settings.SERVICE_CATALOG_URL}/admin/catalog/services/{service_id}",
            json=data,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/services/{service_id}", dependencies=[Depends(admin_required)])
def delete_service(service_id: str):
    """Eliminar servicio (Solo Admin)"""
    try:
        response = requests.delete(
            f"{settings.SERVICE_CATALOG_URL}/admin/catalog/services/{service_id}",
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))