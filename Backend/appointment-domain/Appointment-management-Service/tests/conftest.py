# conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.database import Base, get_db
from app.models.appointment import Appointment
from datetime import datetime
import logging

# DB temporal para tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# -----------------------------
# Fixture de DB para tests
# -----------------------------
@pytest.fixture(scope="function")
def db_session():
    # Crear tablas antes de cada test
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Limpiar tablas para el siguiente test
        Base.metadata.drop_all(bind=engine)

# -----------------------------
# Reemplazar get_db
# -----------------------------
@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

# -----------------------------
# Silenciar logs de Kafka
# -----------------------------
@pytest.fixture(autouse=True)
def silence_logs():
    logging.getLogger("app.core.kafka").setLevel(logging.CRITICAL)

# -----------------------------
# Función auxiliar para crear citas
# -----------------------------
def create_test_appointment(db_session, **kwargs):
    appointment = Appointment(
        id=kwargs.get("id"),
        user_id=kwargs.get("user_id", "user123"),
        service_id=kwargs.get("service_id", "service123"),
        scheduled_time=kwargs.get("scheduled_time", datetime(2026, 1, 18, 10, 0, 0)),
        status=kwargs.get("status", "scheduled")
    )
    db_session.add(appointment)
    db_session.commit()
    db_session.refresh(appointment)
    return appointment
