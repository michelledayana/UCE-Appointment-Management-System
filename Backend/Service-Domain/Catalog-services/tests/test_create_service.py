from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)


@patch("app.application.commands.create_service.services_collection")
def test_create_service(mock_collection):
    mock_result = MagicMock()
    mock_result.inserted_id = "fake_id"
    mock_collection.insert_one.return_value = mock_result

    payload = {
        "name": "Consulta General",
        "description": "Consulta médica básica",
        "student_price": 5,
        "general_price": 10
    }

    response = client.post(
        "/admin/catalog/services",
        json=payload
    )

    assert response.status_code == 201
    assert response.json()["message"] == "Service created successfully"
