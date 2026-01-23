# Availability Validation Service

## 📋 Description
Service responsible for **validating service availability** before appointment creation. Checks Redis cache first for speed, falls back to MongoDB for persistence. Publishes availability events via Kafka for real-time UI updates.

---

## 🏗️ Architecture Used

**Cache-Aside Pattern + Event-Driven**

```
┌──────────────────────────────────────────────────┐
│         Kafka Consumer                           │
│    (consume availability events)                 │
└────────────────┬─────────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────────┐
│         Validation Service Layer                 │
│    - Cache lookup (Redis)                        │
│    - Fallback to MongoDB                         │
│    - Publish result events                       │
└────────────────┬─────────────────────────────────┘
                 │
       ┌─────────┴──────────┬──────────┐
       │                    │          │
  ┌────▼────┐         ┌────▼──┐   ┌──▼────┐
  │ Redis   │        │MongoDB │   │ Kafka │
  │(Cache)  │        │(Source)│   │(Events)
  └──────────┘        └───────┘   └───────┘
```

**Why This Architecture:**
- ✅ **Cache-Aside**: Fast response from Redis
- ✅ **MongoDB**: Flexible schema for availability data
- ✅ **Kafka**: Publish availability changes
- ✅ **Resilient**: Falls back if cache misses

---

## 🎯 Design Principles

| Principle | Application | Benefit |
|-----------|---|---|
| **Cache-Aside** | Redis with MongoDB fallback | High performance |
| **Event-Driven** | Publish validation results | Reactive system |
| **Resilience** | Fallback to MongoDB | No single point of failure |
| **Time-to-Live** | Redis TTL for freshness | Auto-expiring cache |
| **Async Processing** | Kafka for events | Non-blocking validation |

---

## 💾 Database

**Redis (Cache) + MongoDB (Source of Truth)**

```javascript
// MongoDB - availability collection
{
  "_id": ObjectId(),
  "service_id": "service-uuid",
  "available": true,
  "capacity": 50,
  "booked": 12,
  "created_at": ISODate(),
  "updated_at": ISODate()
}
```

```bash
# Redis - availability cache (30 min TTL)
KEY: availability:service-uuid
VALUE: { "available": true, "capacity": 50 }
TTL: 1800 seconds
```

**Why Both:**
- **Redis**: Sub-millisecond lookups for real-time validation
- **MongoDB**: Flexible schema for availability metadata
- **Fallback**: If cache misses, load from MongoDB

---

## 🧪 Testing

**Test Suite:**
```bash
pytest tests/ -v --cov=app
```

| Test | Location | Tests |
|------|-----------|-----------|
| **Unit Tests** | `test_validation_service.py` | Business logic |
| **Cache Tests** | Various test files | Redis interaction |
| **MongoDB Tests** | Various test files | Fallback logic |

**Example:**
```python
def test_validate_availability_cache_hit(service_id, mock_redis):
    mock_redis.get.return_value = {"available": True}
    result = validate_availability(service_id)
    assert result is True
    mock_redis.get.assert_called_once()
```

---

## 📁 Project Structure

```
availability-validation-service/
├── app/
│   ├── config.py                        # Settings
│   ├── main.py                          # FastAPI + consumer startup
│   ├── cache/
│   │   └── redis_client.py              # Redis connection
│   ├── consumers/
│   │   └── availability_consumer.py     # Kafka consumer
│   ├── database/
│   │   └── mongo.py                     # MongoDB connection
│   ├── producers/
│   │   └── availability_producer.py     # Kafka producer
│   ├── schemas/
│   │   └── availability_event.py        # Event schemas
│   └── services/
│       └── validation_service.py        # Business logic
├── tests/
│   ├── __init__.py
│   └── test_validation_service.py
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
python -m app.main
```

---

## 📊 Event Flow

**Availability Check Request:**
```json
{
  "service_id": "service-123",
  "requested_slots": 2
}
```

**Validation Result:**
```json
{
  "service_id": "service-123",
  "available": true,
  "available_slots": 8,
  "checked_at": "2026-01-25T10:20:30Z"
}
```

---

## 📌 Technology Stack

| Component | Technology |
|-----------|-----------|
| Framework | FastAPI |
| Cache | Redis |
| Persistence | MongoDB |
| Event Stream | Kafka |
| Validation | Pydantic |
| Testing | Pytest |
| Container | Docker & Docker Compose |

---

**v1.0.0** | January 2026
