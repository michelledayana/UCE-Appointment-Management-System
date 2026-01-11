from sqlalchemy.orm import Session
from app.db.models import Appointment
from app.schemas.appointment import AppointmentCreate

from app.kafka.producer import publish_appointment_created as kafka_publish
from app.mqtt.mqtt_client import publish_appointment_created as mqtt_publish


from app.db.models import Appointment
from sqlalchemy.orm import Session

def create_appointment(data, db: Session):
    appointment = Appointment(
        user_id=data.user_id,
        service_id=data.service_id,
        scheduled_time=data.scheduled_time
    )

    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    event = {
        "event": "appointment.created",
        "id": str(appointment.id),
        "user_id": appointment.user_id,
        "service_id": appointment.service_id,
        "scheduled_time": appointment.scheduled_time.isoformat(),
        "status": appointment.status,
        "created_at": appointment.created_at.isoformat()
    }

    # 🔐 Eventos NO críticos
    try:
        kafka_publish(event)
    except Exception:
        pass

    try:
        mqtt_publish(event)
    except Exception:
        pass

    return appointment
