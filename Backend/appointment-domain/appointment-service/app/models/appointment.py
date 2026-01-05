from uuid import UUID
from datetime import date, time
from pydantic import BaseModel


class Appointment(BaseModel):
    id: UUID
    service: str
    date: date
    time: time
