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


def test_get_profile_success(mock_db):
    mock_db.query().filter().first.return_value = fake_profile()

    response = client.get("/profiles/andrea@gmail.com")

    assert response.status_code == 200
    assert response.json()["email"] == "andrea@gmail.com"
    assert response.json()["full_name"] == "Andrea Sanchez"


def test_get_profile_not_found(mock_db):
    mock_db.query().filter().first.return_value = None

    response = client.get("/profiles/notfound@gmail.com")

    assert response.status_code == 404
    assert response.json()["detail"] == "Profile not found"
