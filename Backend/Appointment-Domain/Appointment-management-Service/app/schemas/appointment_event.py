from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class AppointmentCreatedEvent(BaseModel):
    id: UUID
    user_id: str
    service_id: str
    scheduled_time: datetime
    status: str
