# Scheduling Management Service

## 📋 Description
Service responsible for **managing service schedules and time slots**. Provides endpoints to create, update, and retrieve availability schedules. Integrates with WebSocket for real-time availability updates to connected clients.

---

## 🏗️ Architecture Used

**Layered Architecture + WebSocket Real-Time**

```
┌──────────────────────────────────────────────────┐
│         REST API + WebSocket                     │
│         (POST/GET /schedules, WS /availability)  │
└────────────────┬─────────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────────┐
│         Service Layer                            │
│         - Schedule CRUD logic                    │
│         - WebSocket message handling             │
└────────────────┬─────────────────────────────────┘
                 │
       ┌─────────┴──────────────┐
       │                        │
  ┌────▼────┐           ┌──────▼─────┐
  │PostgreSQL│           │ WebSocket  │
  │(Schedules)          │(Real-time) │
  └──────────┘           └────────────┘
```

**Why This Architecture:**
- ✅ **REST for CRUD**: Standard operations via HTTP
- ✅ **WebSocket**: Real-time updates without polling
- ✅ **Stateful Connections**: Maintains client connections
- ✅ **Scalable**: Connection manager abstracts complexity

---

## 🎯 Design Principles

| Principle | Application | Benefit |
|-----------|---|---|
| **Layered** | API → Service → DB | Clear responsibilities |
| **WebSocket** | Persistent connections | Real-time updates |
| **Connection Manager** | Centralized connection handling | Scalable broadcasting |
| **Stateless Service** | No server-side state | Easy to scale |
| **Event Broadcasting** | Push updates to subscribers | Low latency |

---

## 💾 Database

**PostgreSQL 15** (Schedule Management)

```sql
CREATE TABLE schedules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    service_id UUID NOT NULL,
    date DATE NOT NULL,
    time_slot VARCHAR(10) NOT NULL,
    available BOOLEAN DEFAULT TRUE,
    capacity INT DEFAULT 10,
    booked INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(service_id, date, time_slot)
);

-- Indexes for performance
CREATE INDEX idx_service_schedule ON schedules(service_id, date);
CREATE INDEX idx_availability ON schedules(available, date);
```

**Why PostgreSQL:**
- Strong ACID guarantees for bookings
- Unique constraints prevent double-booking
- Transaction support for atomic operations

---
## 🧪 Testing

**Test Suite:**
```bash
pytest tests/ -v --cov=app
```

| Test | Location | Tests |
|------|-----------|-----------|
| **Controller Tests** | `test_schedule_controller.py` | Endpoint logic |
| **Service Tests** | `test_schedule_service.py` | Business logic |

**Example:**
```python
def test_create_schedule(client, auth_headers):
    response = client.post(
        "/schedules",
        json={
            "service_id": "service-123",
            "date": "2026-02-15",
            "time_slot": "09:00",
            "capacity": 10
        },
        headers=auth_headers
    )
    assert response.status_code == 201
```

---

## 📁 Project Structure

```
scheduling-management-service/
├── app/
│   ├── config.py                        # Settings
│   ├── main.py                          # FastAPI + CORS
│   ├── controllers/
│   │   └── scheduling_controller.py     # REST endpoints
│   ├── database/
│   │   ├── db.py                        # Connection
│   │   └── dependencies.py              # DB session dependency
│   ├── models/
│   │   └── schedule_model.py            # ORM models
│   ├── schemas/
│   │   └── schedule_schema.py           # Pydantic schemas
│   ├── services/
│   │   └── schedule_service.py          # Business logic
│   └── websocket/
│       ├── availability_events.py       # Event schemas
│       └── connection_manager.py        # Connection handling
├── tests/
│   ├── test_schedule_controller.py
│   └── test_schedule_service.py
├── requirements.txt
├── docker-compose.yml
└── .env
```

---

## 🚀 How to Run

**Docker:**
```bash
docker-compose up -d
```

**Local:**
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8090
pytest tests/ -v
```

---

## 📊 Endpoints

**Create Schedule:**
```bash
POST /schedules
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "service_id": "service-123",
  "date": "2026-02-15",
  "time_slot": "09:00",
  "capacity": 10
}
```

**List Schedules:**
```bash
GET /schedules?service_id=service-123&date=2026-02-15
Authorization: Bearer <jwt_token>
```

**WebSocket - Real-Time Updates:**
```javascript
const ws = new WebSocket('wss://host/ws/availability');
ws.onmessage = (event) => {
  const update = JSON.parse(event.data);
  console.log(`Service ${update.service_id} now has ${update.available_slots} slots`);
};
```

---

## 📌 Technology Stack

| Component | Technology |
|-----------|-----------|
| Framework | FastAPI |
| DB | PostgreSQL 15 |
| ORM | SQLAlchemy 2.0+ |
| Real-time | WebSocket |
| Validation | Pydantic |
| Testing | Pytest |
| Container | Docker & Docker Compose |

---

**v1.0.0** | January 2026
