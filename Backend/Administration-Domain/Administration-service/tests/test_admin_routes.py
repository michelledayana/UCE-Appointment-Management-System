from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_admin_health():
    response = client.get("/admin/health")

    assert response.status_code == 200
    assert response.json() == {
        "service": "administration-service",
        "status": "ok"
    }
