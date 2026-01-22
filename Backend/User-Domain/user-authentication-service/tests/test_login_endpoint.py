from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)


class FakeUser:
    def __init__(self):
        self.email = "test@gmail.com"
        self.user_type = "GENERAL"
        self.password_hash = "fakehash"


@patch("app.controllers.auth_controller.authenticate_user")
def test_login_success(mock_auth):
    mock_auth.return_value = FakeUser()

    payload = {
        "email": "test@gmail.com",
        "password": "Test1234"
    }

    response = client.post("/auth/login", json=payload)

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


@patch("app.controllers.auth_controller.authenticate_user")
def test_login_invalid_credentials(mock_auth):
    mock_auth.return_value = None

    payload = {
        "email": "wrong@gmail.com",
        "password": "wrong"
    }

    response = client.post("/auth/login", json=payload)

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"
