from app.kafka.consumer import SERVICE_CACHE
import pytest

def pytest_sessionstart():
    SERVICE_CACHE.clear()
    SERVICE_CACHE["svc-123"] = {
        "service_id": "svc-123",
        "name": "Consulta General",
        "price": 10
    }
