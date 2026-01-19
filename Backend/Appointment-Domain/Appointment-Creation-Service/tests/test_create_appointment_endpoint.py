import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_appointment_endpoint():
    payload = {
        "user_id": "user-789",
        "service_id": "service-999",
        "scheduled_at": "2026-01-21T15:30:00"  # corregido
    }
    response = client.post("/appointments", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == "user-789"
    assert data["service_id"] == "service-999"
    assert data["scheduled_at"] == "2026-01-21T15:30:00"
