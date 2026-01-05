from datetime import date, time
from pydantic import BaseModel


class AppointmentCreate(BaseModel):
    service: str
    date: date
    time: time
