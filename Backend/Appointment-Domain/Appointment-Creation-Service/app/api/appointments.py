from fastapi import APIRouter, HTTPException
from app.schemas.appointment import AppointmentCreate, AppointmentResponse
from app.services.appointment_service import create_appointment_service

router = APIRouter()

@router.post("/", response_model=AppointmentResponse, status_code=201)
def create_appointment(appointment: AppointmentCreate):
    # Lógica de creación de cita (mock para tests)
    try:
        result = create_appointment_service(appointment)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
