from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Optional

from app.db.database import get_db
from app.models.appointment import Appointment
from app.schemas.appointment import AppointmentResponse

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)

@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_appointment_by_id(
    appointment_id: UUID,
    db: Session = Depends(get_db)
):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    return appointment


@router.get("/", response_model=List[AppointmentResponse])
def get_appointments(
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Appointment)

    if status:
        query = query.filter(Appointment.status == status)

    return query.all()


@router.get("/user/{user_id}", response_model=List[AppointmentResponse])
def get_appointments_by_user(
    user_id: str,
    db: Session = Depends(get_db)
):
    return db.query(Appointment).filter(
        Appointment.user_id == user_id
    ).all()


@router.get("/service/{service_id}", response_model=List[AppointmentResponse])
def get_appointments_by_service(
    service_id: str,
    db: Session = Depends(get_db)
):
    return db.query(Appointment).filter(
        Appointment.service_id == service_id
    ).all()
