# app/db/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

Base = declarative_base()

# Detectar si estamos en modo test
USE_SQLITE = os.getenv("TEST_SQLITE", "0") == "1"

if USE_SQLITE:
    # SQLite en memoria para tests
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
else:
    # Postgres para producción
    engine = create_engine(settings.database_url)

# Session factory para la app
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Función de utilidad para dependencias de FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
