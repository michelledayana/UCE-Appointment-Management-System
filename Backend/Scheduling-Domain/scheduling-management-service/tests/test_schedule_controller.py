from fastapi.testclient import TestClient
from app.main import app
from datetime import date

client = TestClient(app)


def test_create_schedule_endpoint():
    payload = {
        "service_id": "dentistry",
        "date": "2026-01-20",
        "time_slot": "09:00-10:00"
    }

    response = client.post("/schedules/", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert data["service_id"] == "dentistry"
    assert data["date"] == "2026-01-20"
    assert data["time_slot"] == "09:00-10:00"
    assert data["available"] is True
    assert "id" in data
