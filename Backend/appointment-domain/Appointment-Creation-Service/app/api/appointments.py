from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.appointment import AppointmentCreate, AppointmentResponse
from app.services.appointment_service import create_appointment
from app.db.database import get_db

router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.post("/", response_model=AppointmentResponse)
def create(
    data: AppointmentCreate,
    db: Session = Depends(get_db)
):
    return create_appointment(data, db)
