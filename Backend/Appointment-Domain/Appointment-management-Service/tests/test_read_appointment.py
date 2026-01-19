from uuid import uuid4
from datetime import datetime
from app.models.appointment import Appointment

def test_read_appointment_not_found(client):
    response = client.get(f"/appointments/{uuid4()}")
    assert response.status_code == 404

def test_read_appointment_found(client, db_session):
    # Insertar una cita de prueba con datetime correcto
    appointment = Appointment(
        id=uuid4(),
        user_id="user123",
        service_id="service123",
        scheduled_time=datetime(2026, 1, 18, 10, 0, 0),
        status="scheduled"
    )
    db_session.add(appointment)
    db_session.commit()

    response = client.get(f"/appointments/{appointment.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(appointment.id)
    assert data["user_id"] == "user123"
