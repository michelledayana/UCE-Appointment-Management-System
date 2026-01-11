from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.database import get_db
from app.models.appointment import Appointment
from app.schemas.appointment import AppointmentResponse, UpdateAppointmentStatus

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)


@router.patch("/{appointment_id}", response_model=AppointmentResponse)
def update_status(
    appointment_id: UUID,
    body: UpdateAppointmentStatus,
    db: Session = Depends(get_db)
):
    appointment = (
        db.query(Appointment)
        .filter(Appointment.id == appointment_id)
        .first()
    )

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    appointment.status = body.status
    db.commit()
    db.refresh(appointment)

    return appointment
