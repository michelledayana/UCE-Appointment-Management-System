from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from datetime import datetime
from db.database import Base

class UserReference(Base):
    """Local reference of users to validate appointments and prices"""
    __tablename__ = "user_references"
    email = Column(String, primary_key=True)
    user_type = Column(String) # To know if we charge Student or General price

class Appointment(Base):
    """Main appointment table"""
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, ForeignKey("user_references.email"))
    service_name = Column(String) # e.g., "Medical Checkup", "Library Access"
    appointment_date = Column(DateTime)
    price = Column(Float)
    status = Column(String, default="SCHEDULED") # SCHEDULED, COMPLETED, CANCELLED
    created_at = Column(DateTime, default=datetime.utcnow)