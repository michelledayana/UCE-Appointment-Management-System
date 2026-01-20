import pytest
from uuid import uuid4
from datetime import datetime
from app.models.appointment import Appointment
from app.services.appointment_service import create_appointment, get_appointment

def test_create_appointment(db_session):
    appointment = Appointment(
        id=str(uuid4()),
        user_id=str(uuid4()),
        service_id=str(uuid4()),
        scheduled_time=datetime.utcnow()
    )
    created = create_appointment(db_session, appointment)
    assert created.id == appointment.id
    assert created.status == "scheduled"

def test_get_appointment(db_session):
    appointment = Appointment(
        id=str(uuid4()),
        user_id=str(uuid4()),
        service_id=str(uuid4()),
        scheduled_time=datetime.utcnow()
    )
    db_session.add(appointment)
    db_session.commit()

    fetched = get_appointment(db_session, appointment.id)
    assert fetched is not None
    assert fetched.id == appointment.id
