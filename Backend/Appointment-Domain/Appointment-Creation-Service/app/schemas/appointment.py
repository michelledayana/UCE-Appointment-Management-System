from pydantic import BaseModel
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class AppointmentCreate(BaseModel):
    user_id: str
    service_id: str
    scheduled_at: datetime  # antes era scheduled_time

class AppointmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    service_id: str
    scheduled_at: datetime

   
