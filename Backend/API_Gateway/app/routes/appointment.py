from fastapi import APIRouter, Request, HTTPException
import requests
from app.config import settings

router = APIRouter()

@router.post("/")
def create_appointment(data: dict, request: Request):
    """Crear nueva cita"""
    try:
        response = requests.post(
            f"{settings.APPOINTMENT_CREATION_URL}/appointments",
            json=data,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
def list_appointments():
    """Listar todas las citas (Admin)"""
    try:
        response = requests.get(
            f"{settings.APPOINTMENT_MANAGEMENT_URL}/appointments",
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/my")
def my_appointments(request: Request):
    """Obtener citas del usuario autenticado"""
    try:
        # Obtener user_id del token
        user = request.state.user
        user_id = user.get("user_id") or user.get("sub") or user.get("id")
        
        response = requests.get(
            f"{settings.APPOINTMENT_QUERY_URL}/appointments/user/{user_id}",
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{appointment_id}")
def get_appointment(appointment_id: str):
    """Obtener cita por ID"""
    try:
        response = requests.get(
            f"{settings.APPOINTMENT_MANAGEMENT_URL}/appointments/{appointment_id}",
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{appointment_id}")
def update_appointment(appointment_id: str, data: dict):
    """Actualizar estado de cita"""
    try:
        response = requests.patch(
            f"{settings.APPOINTMENT_MANAGEMENT_URL}/appointments/{appointment_id}",
            json=data,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{appointment_id}")
def cancel_appointment(appointment_id: str):
    """Cancelar cita"""
    try:
        response = requests.patch(
            f"{settings.APPOINTMENT_MANAGEMENT_URL}/appointments/{appointment_id}",
            json={"status": "cancelled"},
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/availability")
def check_availability(serviceId: str = None, date: str = None):
    """Verificar disponibilidad"""
    try:
        response = requests.get(
            f"{settings.AVAILABILITY_SERVICE_URL}/availability",
            params={"serviceId": serviceId, "date": date},
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        # Si el servicio no está disponible, devolver slots de ejemplo
        return {
            "availableSlots": [
                "09:00", "10:00", "11:00", 
                "14:00", "15:00", "16:00"
            ]
        }