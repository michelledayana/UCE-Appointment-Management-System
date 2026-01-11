from fastapi import APIRouter
import requests
from app.config import settings

router = APIRouter()

@router.post("/")
def create_appointment(data: dict):
    return requests.post(
        f"{settings.APPOINTMENT_CREATE_URL}/appointments",
        json=data
    ).json()

@router.get("/")
def list_appointments():
    return requests.get(
        f"{settings.APPOINTMENT_MANAGEMENT_URL}/appointments"
    ).json()

@router.get("/{appointment_id}")
def get_appointment(appointment_id: str):
    return requests.get(
        f"{settings.APPOINTMENT_QUERY_URL}/appointments/{appointment_id}"
    ).json()

@router.patch("/{appointment_id}")
def update_appointment(appointment_id: str, data: dict):
    return requests.patch(
        f"{settings.APPOINTMENT_MANAGEMENT_URL}/appointments/{appointment_id}",
        json=data
    ).json()

@router.get("/user/{user_id}")
def appointments_by_user(user_id: str):
    return requests.get(
        f"{settings.APPOINTMENT_QUERY_URL}/appointments/user/{user_id}"
    ).json()
