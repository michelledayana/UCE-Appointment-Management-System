# Appointment Creation Service

## 📋 Description
Specialized service for **creating and registering new appointments**. Validates availability, persists data to PostgreSQL with guaranteed ACID consistency, and publishes events for asynchronous synchronization with other services (Management Service, real-time notifications).

---

## 🏗️ Architecture Used

**Layered Architecture (N-Tier) + Event-Driven Publishing**

```
┌──────────────────────────────────────────────────┐
│         API Layer (FastAPI)                      │
│         POST /appointments                       │
└────────────────┬─────────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────────┐
│         Service Layer (Business Logic)           │
│         create_appointment_service()             │
│         - Pydantic Validation                    │
│         - Business Rules                         │
└────────────────┬─────────────────────────────────┘
                 │
       ┌─────────┴──────────┬──────────┐
       │                    │          │
  ┌────▼────┐         ┌────▼──┐   ┌──▼────┐
  │PostgreSQL│        │Kafka  │   │ MQTT  │
  │ (Write)  │        │(Event)│   │(Real) │
  └──────────┘        └───────┘   └───────┘
```

**Why This Architecture:**
- ✅ **Layers**: Clear separation of concerns
- ✅ **PostgreSQL**: ACID = guaranteed consistent writes
- ✅ **Kafka**: Asynchronous decoupling with other services
- ✅ **MQTT**: Real-time notifications to frontend

---

## 🎯 Design Principles

| Principle | Application | Benefit |
|-----------|---|---|
| **SOLID-SRP** | One class, one responsibility | Easy to maintain and test |
| **SOLID-DIP** | Dependency injection | Loose coupling |
| **Domain-Driven** | Schemas with validations | Guaranteed valid data |
| **Event-Driven** | Kafka for decoupling | Scalable |
| **ACID** | PostgreSQL transactions | Guaranteed consistency |

---

## 💾 Database

**PostgreSQL 15** (Relational - ACID)

```sql
CREATE TABLE appointments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    service_id UUID NOT NULL REFERENCES services(id),
    scheduled_time TIMESTAMP NOT NULL,
    status VARCHAR(50) DEFAULT 'scheduled',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_appointments (user_id),
    INDEX idx_service_appointments (service_id)
);
```

**Why PostgreSQL:**
- ACID transactions = guaranteed atomicity
- Foreign keys = referential integrity
- JSONB = flexible data structure

---

## 🔒 Security

```
Client → HTTPS (TLS 1.3) → ALB + Cloudflare Firewall 
         ↓
      EC2 Bastion/Jump Box (SSH Key Auth)
         ↓
      Private VPC Subnet
         ↓
      Appointment Creation Service


---
## 🧪 Testing
---

**Test Suite:**
```bash
pytest tests/ -v --cov=app
```

| Test | Location | Tests |
|------|-----------|-----------|
| **Unit Tests** | `test_appointment_service.py` | Business logic |
| **Integration** | `test_create_appointment_endpoint.py` | API + PostgreSQL |
| **Kafka** | `test_kafka_consumer_integration.py` | Event publishing |

**Example:**
```python
def test_create_appointment_success(client, mock_db):
    response = client.post(
        "/appointments",
        json={
            "user_id": "user123",
            "service_id": "service456",
            "scheduled_at": "2026-02-15T10:00:00Z"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "scheduled"
    assert "id" in data
```

---

## 📁 Project Structure

```
Appointment-Creation-Service/
├── app/
│   ├── api/
│   │   └── appointments.py              # POST /appointments
│   ├── services/
│   │   └── appointment_service.py       # Business logic
│   ├── db/
│   │   ├── models.py                    # ORM models
│   │   ├── database.py                  # PostgreSQL connection
│   │   └── init_db.py                   # Migrations
│   ├── schemas/
│   │   └── appointment.py               # Pydantic validation
│   ├── kafka/
│   │   ├── producer.py                  # Publish events
│   │   └── consumer.py                  # Listen to events
│   ├── mqtt/
│   │   └── mqtt_client.py               # Real-time notifications
│   ├── config.py                        # Pydantic Settings
│   └── main.py                          # FastAPI app
├── tests/
│   ├── test_appointment_service.py
│   ├── test_create_appointment_endpoint.py
│   └── test_kafka_consumer_integration.py
├── requirements.txt
├── docker-compose.yml
└── .env
```

---

## 🚀 How to Run

**Docker (Recommended):**
```bash
docker-compose up -d
```

**Local Development:**
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8087
pytest tests/ -v
```

---

## 📊 Endpoint

**Create Appointment:**
```bash
POST /appointments
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "service_id": "550e8400-e29b-41d4-a716-446655440001",
  "scheduled_at": "2026-02-15T14:30:00Z"
}
```

**Response (201):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440002",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "service_id": "550e8400-e29b-41d4-a716-446655440001",
  "scheduled_at": "2026-02-15T14:30:00Z",
  "status": "scheduled",
  "created_at": "2026-01-25T10:20:30Z"
}
```

---

## 📌 Technology Stack

| Component | Technology |
|-----------|-----------|
| Framework | FastAPI |
| DB | PostgreSQL 15 |
| ORM | SQLAlchemy 2.0+ |
| Validation | Pydantic 2.0+ |
| Event Stream | Kafka |
| Notifications | MQTT (HiveMQ) |
| Testing | Pytest |
| Container | Docker & Docker Compose |

---

