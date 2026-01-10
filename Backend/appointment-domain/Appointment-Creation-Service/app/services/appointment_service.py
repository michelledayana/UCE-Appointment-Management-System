from app.kafka.producer import publish_appointment_created
from app.mqtt.mqtt_client import publish_notification

def create_appointment(data):
    appointment = {
        "user_id": data.user_id,
        "service_id": data.service_id,
        "time_slot": data.time_slot,
        "status": "CREATED"
    }

    # Kafka (crítico)
    publish_appointment_created(appointment)

    # MQTT (notificación)
    publish_notification({
        "event": "appointment_created",
        "service_id": data.service_id,
        "time_slot": data.time_slot
    })

    return appointment
