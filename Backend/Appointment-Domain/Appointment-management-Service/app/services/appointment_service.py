from sqlalchemy.orm import Session
from app.models.appointment import Appointment
from uuid import UUID
from datetime import datetime

def get_appointment(db: Session, appointment_id: str | UUID):
    """Obtener una cita por ID"""
    if isinstance(appointment_id, UUID):
        appointment_id = str(appointment_id)
    return db.query(Appointment).filter(Appointment.id == appointment_id).first()

def create_appointment(
    db: Session,
    user_id: str,
    service_id: str,
    scheduled_time: datetime | None = None,
    status: str = "scheduled"
):
    """Crear una nueva cita"""
    if scheduled_time is None:
        scheduled_time = datetime.utcnow()

    appointment = Appointment(
        user_id=user_id,
        service_id=service_id,
        scheduled_time=scheduled_time,
        status=status
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment
