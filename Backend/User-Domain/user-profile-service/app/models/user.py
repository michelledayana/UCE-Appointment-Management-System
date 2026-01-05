from sqlalchemy import Column, Integer, String, DateTime
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String)
    user_type = Column(String)
    created_at = Column(DateTime)
