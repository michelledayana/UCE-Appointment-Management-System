from pydantic import BaseModel

class AvailabilityEvent(BaseModel):
    event: str
    service_id: str
    available: bool
