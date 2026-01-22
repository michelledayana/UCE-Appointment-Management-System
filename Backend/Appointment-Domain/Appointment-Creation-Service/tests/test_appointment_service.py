from app.schemas.appointment import AppointmentCreate
from app.services.appointment_service import create_appointment_service

def test_create_appointment_success():
    data = AppointmentCreate(
        user_id="user-123",
        service_id="service-456",
        scheduled_at="2026-01-20T10:00:00"  # corregido
    )
    result = create_appointment_service(data)
    assert result.user_id == "user-123"
    assert result.service_id == "service-456"
    assert result.scheduled_at.isoformat() == "2026-01-20T10:00:00"

