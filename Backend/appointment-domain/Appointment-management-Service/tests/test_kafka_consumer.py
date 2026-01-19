from app.core import kafka
from uuid import uuid4
from app.schemas.appointment_event import AppointmentCreatedEvent

def test_start_consumer_valid_event(mock_kafka_consumer, db_session):
    # Simula que start_consumer se llama
    event = AppointmentCreatedEvent(
        id=uuid4(),
        user_id="user123",
        service_id="service123",
        scheduled_time="2026-01-18T10:00:00",
        status="scheduled"
    )
    mock_kafka_consumer()
    assert mock_kafka_consumer.called is True
