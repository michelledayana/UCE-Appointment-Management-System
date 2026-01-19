from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.main import app

client = TestClient(app)


def fake_profile():
    profile = MagicMock()
    profile.email = "andrea@gmail.com"
    profile.full_name = "Andrea Sanchez"
    profile.user_type = "GENERAL"
    profile.phone = None
    profile.faculty = None
    profile.career = None
    profile.semester = None
    return profile


def test_update_profile_success(mock_db):
    profile = fake_profile()
    mock_db.query().filter().first.return_value = profile

    payload = {
        "phone": "0999999999",
        "faculty": "Engineering"
    }

    response = client.put("/profiles/andrea@gmail.com", json=payload)

    assert response.status_code == 200
    assert response.json()["message"] == "Profile updated successfully"

    assert profile.phone == "0999999999"
    assert profile.faculty == "Engineering"


def test_update_profile_not_found(mock_db):
    mock_db.query().filter().first.return_value = None

    payload = {
        "phone": "0999999999"
    }

    response = client.put("/profiles/notfound@gmail.com", json=payload)

    assert response.status_code == 404
    assert response.json()["detail"] == "Profile not found"
