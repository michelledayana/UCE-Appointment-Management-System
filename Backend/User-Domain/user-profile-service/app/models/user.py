from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.database import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    user_type = Column(String, nullable=False)

    phone = Column(String, nullable=True)
    faculty = Column(String, nullable=True)
    career = Column(String, nullable=True)
    semester = Column(Integer, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
