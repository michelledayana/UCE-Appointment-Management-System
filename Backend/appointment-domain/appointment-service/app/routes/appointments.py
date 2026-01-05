from fastapi import APIRouter
from uuid import UUID

from app.schemas.appointment import AppointmentCreate
from app.services.appointment_service import AppointmentService

router = APIRouter()


@router.get("/health")
def health():
    return {
        "service": "appointment-service",
        "status": "ok"
    }


@router.post("")
def create_appointment(data: AppointmentCreate):
    return AppointmentService.create_appointment(data)


@router.get("")
def list_appointments():
    return AppointmentService.list_appointments()


@router.get("/{appointment_id}")
def get_appointment(appointment_id: UUID):
    return AppointmentService.get_appointment(appointment_id)
