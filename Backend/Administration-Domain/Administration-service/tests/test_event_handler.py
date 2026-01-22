import pytest
from app.application.handlers.event_handlers import handle_event

class FakeCollection:
    def __init__(self):
        self.inserted = []

    def insert_one(self, document):
        self.inserted.append(document)
        return document

def test_handle_event(monkeypatch):
    fake_collection = FakeCollection()

    # Reemplazamos la colección real por la fake
    monkeypatch.setattr(
        "app.application.handlers.event_handlers.audit_collection",
        fake_collection
    )

    event = {
        "event": "user_registered",
        "source": "user-service",
        "payload": {"email": "test@test.com"}
    }

    handle_event(event)

    assert len(fake_collection.inserted) == 1
    inserted_doc = fake_collection.inserted[0]
    assert inserted_doc["event"] == "user_registered"
    assert inserted_doc["source"] == "user-service"
    assert inserted_doc["payload"]["email"] == "test@test.com"
