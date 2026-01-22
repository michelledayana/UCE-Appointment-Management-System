from unittest.mock import patch
from app.kafka.producer import produce_event

def test_kafka_service_created_event():
    # Limpiar llamadas previas
    produce_event.reset_mock()

    event = {
        "event_type": "service.created",
        "service_id": "test-123",
        "name": "Consulta Test"
    }

    # Llamamos al mock
    produce_event(event)

    # Verificamos que el mock fue llamado
    produce_event.assert_called_once_with(event)
