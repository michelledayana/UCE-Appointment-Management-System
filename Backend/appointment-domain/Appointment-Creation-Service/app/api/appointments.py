from fastapi import APIRouter
from app.schemas.appointment import AppointmentCreate
from app.services.appointment_service import create_appointment

router = APIRouter()

@router.post("/appointments")
def create(data: AppointmentCreate):
    return create_appointment(data)
