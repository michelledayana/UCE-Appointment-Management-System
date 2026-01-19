from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

client = TestClient(app)


# -------------------------------
# Test: Registro exitoso
# -------------------------------
@patch("app.services.user_service.publish_user_registered_event")
@patch("app.repositories.user_repository.UserRepository.save")
@patch("app.repositories.user_repository.UserRepository.get_by_email")
@patch("sqlalchemy.orm.session.Session.refresh")
def test_register_user_success(
    mock_refresh,
    mock_get_by_email,
    mock_save,
    mock_kafka
):
    # Email no existe
    mock_get_by_email.return_value = None

    # Simulamos save en DB
    def fake_save(db, user):
        user.id = 1
        user.user_type = "GENERAL"
    mock_save.side_effect = fake_save
    mock_refresh.return_value = None

    payload = {
        "full_name": "Andrea Sanchez",
        "email": "andreasanchez@gmail.com",
        "password": "Andrea1234"
    }

    response = client.post("/users/register", json=payload)

    assert response.status_code == 201
    assert response.json()["status"] == "success"
    assert response.json()["data"]["email"] == "andreasanchez@gmail.com"


# -------------------------------
# Test: Email ya registrado
# -------------------------------
@patch("app.services.user_service.publish_user_registered_event")
@patch("app.repositories.user_repository.UserRepository.get_by_email")
def test_register_user_email_exists(mock_get_by_email, mock_kafka):
    # Simulamos que el email ya existe
    mock_get_by_email.return_value = True

    payload = {
        "full_name": "Andrea Sanchez",
        "email": "andreasanchez@gmail.com",
        "password": "Andrea1234"
    }

    response = client.post("/users/register", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


# -------------------------------
# Test: Kafka falla pero registro exitoso
# -------------------------------
@patch("app.services.user_service.publish_user_registered_event", side_effect=Exception("Kafka down"))
@patch("app.repositories.user_repository.UserRepository.save")
@patch("app.repositories.user_repository.UserRepository.get_by_email")
@patch("sqlalchemy.orm.session.Session.refresh")
def test_register_user_kafka_failure(
    mock_refresh,
    mock_get_by_email,
    mock_save,
    mock_kafka
):
    # Email no existe
    mock_get_by_email.return_value = None

    # Simulamos save en DB
    def fake_save(db, user):
        user.id = 2
        user.user_type = "GENERAL"
    mock_save.side_effect = fake_save
    mock_refresh.return_value = None

    payload = {
        "full_name": "Carlos Perez",
        "email": "carlosperez@gmail.com",
        "password": "Carlos1234"
    }

    response = client.post("/users/register", json=payload)

    # Registro aún exitoso, aunque Kafka falle
    assert response.status_code == 201
    assert response.json()["data"]["email"] == "carlosperez@gmail.com"
