from app.database.mongo import audit_collection
from datetime import datetime

def handle_event(event: dict):
    audit_collection.insert_one({
        "event": event.get("event"),
        "source": event.get("source"),
        "timestamp": datetime.utcnow(),
        "payload": event.get("payload", {})
    })
