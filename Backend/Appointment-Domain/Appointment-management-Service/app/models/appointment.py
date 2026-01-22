# app/models/appointment.py
import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from datetime import datetime
import os
from app.models.base import Base

USE_SQLITE = os.getenv("TEST_SQLITE", "0") == "1"

class Appointment(Base):
    __tablename__ = "appointments"

    if USE_SQLITE:
        id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
        user_id = Column(String(36), nullable=False)
        service_id = Column(String(36), nullable=False)
    else:
        id = Column(PG_UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
        user_id = Column(PG_UUID(as_uuid=True), nullable=False)
        service_id = Column(PG_UUID(as_uuid=True), nullable=False)

    scheduled_time = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default="scheduled")
