import uuid
from app.schemas.schedule_schema import ScheduleCreate


def create_schedule(schedule: ScheduleCreate):
    return {
        "id": str(uuid.uuid4()),
        "service_id": schedule.service_id,
        "date": schedule.date,
        "time_slot": schedule.time_slot,
        "available": True
    }
