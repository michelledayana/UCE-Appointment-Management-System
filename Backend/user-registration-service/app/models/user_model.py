from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from app.database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(100), nullable=False)

    email = Column(String(255), unique=True, nullable=False)

    password_hash = Column(String(255), nullable=False)

    # 👇 Roles controlados (evita errores de escritura)
    user_type = Column(
        Enum("STUDENT", "GENERAL", "ADMIN", name="user_roles"),
        nullable=False,
        default="GENERAL"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
