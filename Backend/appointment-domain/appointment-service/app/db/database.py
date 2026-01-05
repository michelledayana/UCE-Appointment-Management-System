from typing import List
from app.models.appointment import Appointment


class InMemoryDatabase:
    def __init__(self):
        self.appointments: List[Appointment] = []


db = InMemoryDatabase()
