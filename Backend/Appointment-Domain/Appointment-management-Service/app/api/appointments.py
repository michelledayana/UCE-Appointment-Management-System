from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from ..db.database import get_db
from ..services.appointment_service import get_appointment
from ..schemas.appointment import AppointmentResponse

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)

@router.get("/{appointment_id}", response_model=AppointmentResponse)
def read_appointment(
    appointment_id: UUID,
    db: Session = Depends(get_db)
):
    appointment = get_appointment(db, appointment_id)
    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )
    return appointment
