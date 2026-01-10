from pydantic import BaseModel

class AppointmentCreate(BaseModel):
    user_id: str
    service_id: str
    time_slot: str
