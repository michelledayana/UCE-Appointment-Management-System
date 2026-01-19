from sqlalchemy import Column, String, DateTime
from datetime import datetime
import uuid
from app.db.database import Base

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False)
    service_id = Column(String, nullable=False)
    scheduled_time = Column(DateTime, nullable=False)
    status = Column(String, default="CREATED")
    created_at = Column(DateTime, default=datetime.utcnow)
