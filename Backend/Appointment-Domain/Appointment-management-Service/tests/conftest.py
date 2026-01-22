import os
import pytest
from fastapi.testclient import TestClient

# Forzar SQLite en memoria para tests
os.environ["TEST_SQLITE"] = "1"

from app.main import app
from app.db.database import Base, engine, get_db, SessionLocal

@pytest.fixture(scope="function")
def db_session():
    """Fixture para sesión de DB en tests con SQLite en memoria"""
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """Fixture de cliente de test de FastAPI"""
    app.dependency_overrides[get_db] = lambda: db_session
    with TestClient(app) as c:
        yield c
