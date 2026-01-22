import json
from unittest.mock import Mock

# Mock del productor Kafka
produce_event = Mock()

def send_event(topic: str, event: dict):
    """
    Función que normalmente enviaría un evento a Kafka.
    Para tests locales solo imprime/loggea.
    """
    print(f"[MOCK] Event sent to topic {topic}: {json.dumps(event)}")
    # También podemos usar produce_event mock para el test
    produce_event(event)
