from uuid import uuid4
from datetime import datetime
from app.models.appointment import Appointment

def test_read_appointments(client, db_session):
    # Crear 2 citas
    appointment1 = Appointment(
        id=str(uuid4()), user_id=str(uuid4()), service_id=str(uuid4()), scheduled_time=datetime.utcnow()
    )
    appointment2 = Appointment(
        id=str(uuid4()), user_id=str(uuid4()), service_id=str(uuid4()), scheduled_time=datetime.utcnow()
    )
    db_session.add_all([appointment1, appointment2])
    db_session.commit()

    response = client.get("/appointments")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
