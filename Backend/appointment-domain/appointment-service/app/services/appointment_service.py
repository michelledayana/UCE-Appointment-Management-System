from uuid import uuid4, UUID
from datetime import date
from fastapi import HTTPException, status

from app.db.database import db
from app.models.appointment import Appointment
from app.schemas.appointment import AppointmentCreate


class AppointmentService:

    @staticmethod
    def create_appointment(data: AppointmentCreate) -> Appointment:
        if data.date < date.today():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Appointment date must be in the future"
            )

        appointment = Appointment(
            id=uuid4(),
            service=data.service,
            date=data.date,
            time=data.time
        )

        db.appointments.append(appointment)
        return appointment

    @staticmethod
    def list_appointments():
        return db.appointments

    @staticmethod
    def get_appointment(appointment_id: UUID):
        for appointment in db.appointments:
            if appointment.id == appointment_id:
                return appointment

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
