from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class UpdateAppointmentStatus(BaseModel):
    status: str


class AppointmentResponse(BaseModel):
    id: UUID               # 🔥 ERA str → ERROR
    user_id: str
    service_id: str
    scheduled_time: datetime
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
