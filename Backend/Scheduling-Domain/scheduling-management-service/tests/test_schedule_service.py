from app.services.schedule_service import create_schedule
from app.schemas.schedule_schema import ScheduleCreate
from datetime import date


def test_create_schedule_success():
    schedule_data = ScheduleCreate(
        service_id="dentistry",
        date=date(2026, 1, 20),
        time_slot="09:00-10:00"
    )

    result = create_schedule(schedule_data)

    assert result["service_id"] == "dentistry"
    assert result["date"] == date(2026, 1, 20)
    assert result["time_slot"] == "09:00-10:00"
    assert result["available"] is True
    assert "id" in result
