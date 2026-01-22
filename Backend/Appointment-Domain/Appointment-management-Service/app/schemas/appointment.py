from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from pydantic import ConfigDict

class AppointmentResponse(BaseModel):
    id: UUID
    user_id: str
    service_id: str
    scheduled_time: datetime
    status: str

    model_config = ConfigDict(from_attributes=True)  # Pydantic v2

