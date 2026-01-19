from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class AppointmentResponse(BaseModel):
    id: UUID
    user_id: str
    service_id: str
    scheduled_time: datetime
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
