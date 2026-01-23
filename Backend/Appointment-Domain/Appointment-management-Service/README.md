# Appointment Management Service

## 📋 Description
Service specialized in **reading and managing appointments** created by other services. Consumes Kafka events, maintains a denormalized read model in PostgreSQL, and provides query endpoints for frontend applications. Implements eventual consistency pattern for high scalability.

---

## 🏗️ Architecture Used

**CQRS Pattern (Command Query Responsibility Segregation) + Event-Sourced**

```
┌──────────────────────────────────────────────────┐
│         Kafka Consumer                           │
│    (appointment.created events)                  │
└────────────────┬─────────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────────┐
│         Service Layer                            │
│    (Event Processing & Validation)               │
└────────────────┬─────────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────────┐
│    PostgreSQL Read Model                         │
│    (Denormalized for queries)                    │
└────────────────┬─────────────────────────────────┘
                 │
    ┌────────────┴────────────┐
    │                         │
┌───▼───────┐           ┌────▼──────┐
│ GET /      │           │ Health    │
│appointments│           │ Checks    │
└────────────┘           └───────────┘
```

**Why This Architecture:**
- ✅ **CQRS**: Separates write (Creation Service) from read (this service)
- ✅ **Eventual Consistency**: Scales better than strong consistency
- ✅ **Denormalized**: Optimized for query performance
- ✅ **Event-Sourced**: Single source of truth in Kafka

---

## 🎯 Design Principles

| Principle | Application | Benefit |
|-----------|---|---|
| **CQRS** | Separate read from write | Independent scaling |
| **Event Sourcing** | Immutable event log | Full audit trail |
| **Eventual Consistency** | Async event processing | Better performance |
| **Repository Pattern** | Data access abstraction | Testable queries |
| **Read Model Optimization** | Indexes on query fields | Fast responses |

---

## 💾 Database

**PostgreSQL 15** (Read-Optimized Model)

```sql
CREATE TABLE appointments_read_model (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    service_id UUID NOT NULL,
    scheduled_time TIMESTAMP NOT NULL,
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes optimized for queries
CREATE INDEX idx_user_appointments ON appointments_read_model(user_id);
CREATE INDEX idx_status ON appointments_read_model(status);
CREATE INDEX idx_scheduled_time ON appointments_read_model(scheduled_time);
```

**Why PostgreSQL for Read Model:**
- Read-optimized indexes for fast queries
- Denormalization allowed for performance
- Eventual consistency acceptable
- Cost-effective for read-heavy workloads

---

## 🔒 Security

```
Client → HTTPS (TLS 1.3) → ALB + Cloudflare Firewall 
         ↓
      EC2 Bastion/Jump Box (SSH Key Auth)
         ↓
      VPC Privada Subnet
         ↓
      Appointment Management Service
```


## 🧪 Testing

**Test Suite:**
```bash
pytest tests/ -v --cov=app
```

| Test | Location | Tests |
|------|-----------|-----------|
| **Unit Tests** | `test_appointment_service.py` | Business logic |
| **Consumer Tests** | `test_kafka_consumer.py` | Event processing |
| **Query Tests** | `test_read_appointment.py` | API queries |

**Example:**
```python
def test_get_user_appointments(client, mock_db):
    response = client.get(
        "/appointments?user_id=user123",
        headers={"Authorization": "Bearer token"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert all(a["user_id"] == "user123" for a in data)
```

---

## 📁 Project Structure

```
Appointment-Management-Service/
├── app/
│   ├── api/
│   │   └── appointments.py              # GET /appointments
│   ├── services/
│   │   └── appointment_service.py       # Read model logic
│   ├── core/
│   │   └── kafka.py                     # Kafka consumer
│   ├── db/
│   │   ├── models.py                    # Read model ORM
│   │   ├── database.py                  # PostgreSQL connection
│   │   ├── init_db.py                   # Schema initialization
│   │   └── session.py                   # DB session management
│   ├── schemas/
│   │   ├── appointment.py               # Pydantic models
│   │   └── appointment_event.py         # Kafka event schema
│   ├── config.py                        # Pydantic Settings
│   └── main.py                          # FastAPI app + Kafka startup
├── tests/
│   ├── test_appointment_service.py
│   ├── test_kafka_consumer.py
│   └── test_read_appointment.py
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
uvicorn app.main:app --reload --port 8088
pytest tests/ -v
```

---

## 📊 Endpoints

**List Appointments (with filters):**
```bash
GET /appointments?user_id=user123&status=scheduled
Authorization: Bearer <jwt_token>
```

**Response (200):**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440002",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "service_id": "550e8400-e29b-41d4-a716-446655440001",
    "scheduled_time": "2026-02-15T14:30:00Z",
    "status": "scheduled",
    "created_at": "2026-01-25T10:20:30Z"
  }
]
```

**Get Single Appointment:**
```bash
GET /appointments/{id}
Authorization: Bearer <jwt_token>
```

---

## 📌 Technology Stack

| Component | Technology |
|-----------|-----------|
| Framework | FastAPI |
| DB (Read Model) | PostgreSQL 15 |
| Event Source | Kafka |
| ORM | SQLAlchemy 2.0+ |
| Validation | Pydantic 2.0+ |
| Testing | Pytest |
| Container | Docker & Docker Compose |

---
