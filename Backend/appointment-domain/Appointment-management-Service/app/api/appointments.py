from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.models.appointment import Appointment
from app.schemas.appointment import AppointmentStatusUpdate, AppointmentResponse
from app.core.kafka import publish_event

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.patch("/{appointment_id}/status", response_model=AppointmentResponse)
def update_status(
    appointment_id: UUID,
    payload: AppointmentStatusUpdate,
    db: Session = Depends(get_db)
):
    appointment = db.get(Appointment, appointment_id)

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    appointment.status = payload.status
    db.commit()
    db.refresh(appointment)

    publish_event("appointment.updated", {
        "id": str(appointment.id),
        "status": appointment.status
    })

    return appointment
