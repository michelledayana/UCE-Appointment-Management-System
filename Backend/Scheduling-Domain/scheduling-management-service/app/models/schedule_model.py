from sqlalchemy import Column, String, Boolean, Date
from app.database.db import Base

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(String, primary_key=True, index=True)
    service_id = Column(String, index=True)
    date = Column(Date)
    time_slot = Column(String)
    available = Column(Boolean, default=True)
