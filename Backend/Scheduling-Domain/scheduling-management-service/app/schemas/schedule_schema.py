from pydantic import BaseModel
from datetime import date


class ScheduleCreate(BaseModel):
    service_id: str
    date: date
    time_slot: str


class ScheduleResponse(BaseModel):
    id: str
    service_id: str
    date: date
    time_slot: str
    available: bool
