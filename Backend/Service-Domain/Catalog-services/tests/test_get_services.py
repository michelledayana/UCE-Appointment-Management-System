from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)


@patch("app.application.queries.get_services.services_collection")
@patch("app.infrastructure.redis.cache.redis_client")
def test_get_catalog_services(mock_redis, mock_mongo):
    """
    Functional test for GET /catalog/services
    External dependencies are mocked (Redis + Mongo)
    """

    # 🔹 Redis cache MISS
    mock_redis.get.return_value = None

    # 🔹 Mongo returns fake data
    mock_mongo.find.return_value = [
        {"id": 1, "name": "Laboratory"},
        {"id": 2, "name": "Dentistry"}
    ]

    response = client.get("/catalog/services")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["name"] == "Laboratory"
