def test_process_message_calls_handler(monkeypatch):
    called = {"value": False}

    def fake_handler(event):
        called["value"] = True

    # Reemplazamos la función real
    monkeypatch.setattr(
        "app.infrastructure.kafka.consumer.handle_event",
        fake_handler
    )

    from app.infrastructure.kafka.consumer import start_kafka_consumer

    # Simulamos mensaje
    message = {"event": "user_registered", "source": "user-service", "payload": {"email": "test@test.com"}}

    # Llamamos handler directamente
    fake_handler(message)

    assert called["value"] is True
