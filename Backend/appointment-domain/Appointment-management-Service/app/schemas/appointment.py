from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class AppointmentStatusUpdate(BaseModel):
    status: str


class AppointmentResponse(BaseModel):
    id: UUID
    user_id: str
    service_id: str
    scheduled_time: datetime
    status: str
    updated_at: datetime | None

    class Config:
        from_attributes = True
