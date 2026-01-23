# Catalog Service

## 📋 Description
Service responsible for **managing the service catalog**. Provides create, read, update, and disable operations for services. Implements hexagonal architecture with CQRS pattern. Caches results in Redis and publishes events via Kafka for updates across the system.

---

## 🏗️ Architecture Used

**Hexagonal Architecture (Ports & Adapters) + CQRS + Caching**

```
┌──────────────────────────────────────────────────┐
│         REST API (Ports)                         │
│         (POST/GET /services)                     │
└────────────────┬─────────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────────┐
│         Application Layer                        │
│         - Command Handlers (Create/Update)       │
│         - Query Handlers (Read)                  │
└────────────────┬─────────────────────────────────┘
                 │
       ┌─────────┴──────────┬──────────┐
       │                    │          │
  ┌────▼────┐         ┌────▼──┐   ┌──▼────┐
  │ MongoDB  │        │Redis  │   │ Kafka │
  │(Persist) │        │(Cache)│   │(Events)
  └──────────┘        └───────┘   └───────┘
```

**Why This Architecture:**
- ✅ **Hexagonal**: Isolates business logic from infrastructure
- ✅ **CQRS**: Commands (Write) separate from Queries (Read)
- ✅ **MongoDB**: Flexible schema for service attributes
- ✅ **Redis**: Fast caching layer for frequent reads
- ✅ **Kafka**: Event propagation for catalog updates

---

## 🎯 Design Principles

| Principle | Application | Benefit |
|-----------|---|---|
| **Hexagonal** | Core logic isolated from adapters | Testable business rules |
| **CQRS** | Separate commands from queries | Optimized for both operations |
| **Cache-Aside** | Redis for hot data | Reduces database load |
| **Event-Driven** | Kafka for updates | Eventual consistency |
| **Domain Events** | Published on changes | Audit trail |

---

## 💾 Database

**MongoDB (Flexible Schema) + Redis Cache**

```javascript
// MongoDB - services collection
{
  "_id": ObjectId(),
  "name": "Haircut Service",
  "description": "Professional haircut service",
  "price": 25.00,
  "duration_minutes": 30,
  "capacity": 5,
  "enabled": true,
  "attributes": {
    "category": "beauty",
    "gender": "unisex"
  },
  "created_at": ISODate(),
  "updated_at": ISODate()
}
```

```bash
# Redis Cache (1 hour TTL)
KEY: service:service-uuid
VALUE: JSON serialized service object
TTL: 3600 seconds
```

**Why MongoDB:**
- Flexible schema for various service types
- JSONB for storing service attributes
- Easy to add new fields without migrations

---

---

## 🧪 Testing

**Test Suite:**
```bash
pytest tests/ -v --cov=app
```

| Test | Location | Tests |
|------|-----------|-----------|
| **Create Service** | `test_create_service.py` | Command handling |
| **Get Services** | `test_get_services.py` | Query handling + cache |

**Example:**
```python
def test_create_service(client, auth_headers):
    response = client.post(
        "/services",
        json={
            "name": "Massage Service",
            "price": 50.00,
            "duration_minutes": 60,
            "capacity": 3
        },
        headers=auth_headers
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Massage Service"
```

---

## 📁 Project Structure

```
Catalog-services/
├── app/
│   ├── config.py                        # Settings
│   ├── main.py                          # FastAPI app
│   ├── api/
│   │   └── rest/
│   │       ├── admin.py                 # Admin endpoints
│   │       └── catalog.py               # Public endpoints
│   ├── application/
│   │   ├── commands/
│   │   │   ├── create_service.py        # Create command
│   │   │   ├── update_service.py        # Update command
│   │   │   └── disable_service.py       # Disable command
│   │   ├── handlers/
│   │   │   ├── command_handlers.py      # Command execution
│   │   │   └── query_handlers.py        # Query execution
│   │   └── queries/
│   │       └── get_services.py          # Query definition
│   ├── infrastructure/
│   │   ├── db/
│   │   │   └── mongo.py                 # MongoDB adapter
│   │   ├── kafka/
│   │   │   └── producer.py              # Kafka producer
│   │   └── redis/
│   │       └── cache.py                 # Redis adapter
│   └── schemas/
│       └── service_schema.py            # Pydantic models
├── tests/
│   ├── test_create_service.py
│   └── test_get_services.py
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
uvicorn app.main:app --reload --port 8091
pytest tests/ -v
```

---

## 📊 Endpoints

**Create Service:**
```bash
POST /services
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "name": "Massage Service",
  "price": 50.00,
  "duration_minutes": 60,
  "capacity": 3,
  "attributes": {"type": "therapeutic"}
}
```

**List Services:**
```bash
GET /services?enabled=true&category=beauty
Authorization: Bearer <jwt_token>
```

**Response (200):**
```json
{
  "total": 15,
  "data": [
    {
      "id": "service-uuid",
      "name": "Massage Service",
      "price": 50.00,
      "duration_minutes": 60,
      "capacity": 3,
      "enabled": true
    }
  ]
}
```

---

## 📌 Technology Stack

| Component | Technology |
|-----------|-----------|
| Framework | FastAPI |
| DB | MongoDB |
| Cache | Redis |
| Event Stream | Kafka |
| Validation | Pydantic |
| Testing | Pytest |
| Container | Docker & Docker Compose |

---

## 🔄 Event Flow

1. **Admin** creates service via REST API
2. **Command Handler** validates input
3. **Service** saved to MongoDB
4. **Cache** invalidated or updated
5. **Kafka Event** published (`service.created`)
6. **Other Services** consume event and react

---

