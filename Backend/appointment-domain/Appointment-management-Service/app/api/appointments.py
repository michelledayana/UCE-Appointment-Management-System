from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.appointment import AppointmentResponse
from app.db.database import get_db
from app.models.appointment import Appointment

router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_appointment(
    appointment_id: str,
    db: Session = Depends(get_db)
):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    return appointment
