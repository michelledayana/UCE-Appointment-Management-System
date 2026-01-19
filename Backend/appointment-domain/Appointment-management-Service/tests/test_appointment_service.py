import pytest
from uuid import uuid4
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.appointment import Base, Appointment
from app.services.appointment_service import get_appointment, create_appointment

# Base de datos SQLite en memoria para pruebas
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()

def test_create_and_get_appointment(db):
    # Crear appointment de prueba
    appointment = Appointment(
        id=uuid4(),
        user_id="user-1",
        service_id="service-1",
        scheduled_time=datetime.utcnow(),
        status="scheduled"
    )
    create_appointment(db, appointment)

    # Recuperar appointment
    retrieved = get_appointment(db, appointment.id)
    assert retrieved.id == appointment.id
    assert retrieved.status == "scheduled"
