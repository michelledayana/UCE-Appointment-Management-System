from fastapi import APIRouter, Depends
import requests
from app.config import settings
from app.security.dependencies import admin_required

router = APIRouter()

@router.get("/services")
def list_services():
    return requests.get(
        f"{settings.CATALOG_SERVICE_URL}/catalog/services"
    ).json()

@router.post("/services", dependencies=[Depends(admin_required)])
def create_service(data: dict):
    return requests.post(
        f"{settings.CATALOG_SERVICE_URL}/admin/catalog/services",
        json=data
    ).json()

@router.put("/services/{service_id}", dependencies=[Depends(admin_required)])
def update_service(service_id: str, data: dict):
    return requests.put(
        f"{settings.CATALOG_SERVICE_URL}/admin/catalog/services/{service_id}",
        json=data
    ).json()

@router.delete("/services/{service_id}", dependencies=[Depends(admin_required)])
def delete_service(service_id: str):
    return requests.delete(
        f"{settings.CATALOG_SERVICE_URL}/admin/catalog/services/{service_id}"
    ).json()
