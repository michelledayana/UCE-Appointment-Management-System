import pytest
from unittest.mock import patch, MagicMock
import json
from uuid import uuid4
from app.core import kafka
from app.models.appointment import Appointment

@pytest.fixture
def mock_kafka_consumer():
    with patch("app.core.kafka.KafkaConsumer") as mock_consumer:
        yield mock_consumer

def test_start_consumer_runs(mock_kafka_consumer):
    # Mensaje de prueba con UUID válido
    mock_message = MagicMock()
    mock_message.value = json.dumps({
        "id": str(uuid4()),
        "user_id": str(uuid4()),
        "service_id": str(uuid4()),
        "scheduled_time": "2026-01-18T10:00:00",
        "status": "scheduled"
    }).encode()

    mock_kafka_consumer.return_value.__iter__.return_value = iter([mock_message])

    # Mock de SessionLocal para DB
    with patch("app.core.kafka.SessionLocal") as mock_session:
        mock_db = MagicMock()
        mock_session.return_value = mock_db

        # Ejecutar start_consumer (usa mock Kafka y mock DB)
        kafka.start_consumer()

        # Comprobaciones
        mock_kafka_consumer.assert_called_once()
        mock_db.merge.assert_called()
        mock_db.commit.assert_called()
