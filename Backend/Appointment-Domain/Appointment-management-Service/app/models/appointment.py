from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    service_id = Column(String, nullable=False)
    scheduled_time = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)
