
from app.database.mongo import audit_collection

def handle_event(event: dict, collection=None):
    """
    Maneja eventos de Kafka y los guarda en MongoDB
    `collection` opcional para inyectar un fake en los tests
    """
    collection = collection or audit_collection

    document = {
        "event": event.get("event"),
        "source": event.get("source"),
        "payload": event.get("payload", {})
    }

    collection.insert_one(document)
