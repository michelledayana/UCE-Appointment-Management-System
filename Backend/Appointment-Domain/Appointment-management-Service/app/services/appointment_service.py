from sqlalchemy.orm import Session
from uuid import UUID
from app.models.appointment import Appointment

def get_appointment(db: Session, appointment_id: UUID):
    return db.query(Appointment).filter(Appointment.id == appointment_id).first()

def create_appointment(db: Session, appointment: Appointment):
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment
