# Appointment Query Service

## 📋 Description
Read-only service optimized for **querying and filtering appointments**. Provides high-performance endpoints for retrieving appointment data with various filters. Acts as a dedicated query facade for the frontend.

---

## 🏗️ Architecture Used

**Query Service Pattern (Read Facade) + Event-Driven**

```
┌──────────────────────────────────────────────────┐
│         Kafka Consumer                           │
│    (appointment events)                          │
└────────────────┬─────────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────────┐
│         Query Service Layer                      │
│    (Filter & format responses)                   │
└────────────────┬─────────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────────┐
│    PostgreSQL (Optimized for queries)            │
│    - Indexes on common filters                   │
│    - Denormalized structure                      │
└────────────────┬─────────────────────────────────┘
                 │
    ┌────────────┴────────────┐
    │                         │
┌───▼───────┐           ┌────▼──────┐
│ GET /     │           │ Health    │
│appointments│           │ Check     │
└────────────┘           └───────────┘
```

**Why This Architecture:**
- ✅ **Separation of Concerns**: Dedicated for queries only
- ✅ **Performance**: Optimized indexes for common queries
- ✅ **Scalability**: Query service scales independently
- ✅ **Read-Only**: No write logic, pure reads

---

## 🎯 Design Principles

| Principle | Application | Benefit |
|-----------|---|---|
| **Query Facade** | Single point for queries | Consistent API |
| **Read Optimization** | Strategic indexing | Fast responses |
| **Filter Abstraction** | Multiple filter params | Flexible queries |
| **Stateless** | No local state | Horizontal scaling |
| **Cache-Ready** | Queryable data | Easy caching |

---

## 💾 Database

**PostgreSQL 15** (Query-Optimized)

```sql
CREATE TABLE appointments (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    service_id UUID NOT NULL,
    scheduled_time TIMESTAMP NOT NULL,
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL
);

-- Query optimization indexes
CREATE INDEX idx_list_appointments ON appointments(user_id, status);
CREATE INDEX idx_search_by_date ON appointments(scheduled_time);
CREATE INDEX idx_service_lookup ON appointments(service_id);
```

**Why PostgreSQL:**
- Powerful WHERE clauses for filtering
- JSONB for flexible queries
- Materialized views for complex aggregations
- Excellent performance for read operations


---

## 🧪 Testing

**Test Suite:**
```bash
pytest tests/ -v
```

| Test | Location | Tests |
|------|-----------|-----------|
| **List Tests** | `test_list_appointments.py` | Filter operations |
| **Query Tests** | Various test files | Different query scenarios |

**Example:**
```python
def test_list_appointments_by_status(client):
    response = client.get(
        "/appointments?status=scheduled",
        headers={"Authorization": "Bearer token"}
    )
    assert response.status_code == 200
    assert all(a["status"] == "scheduled" for a in response.json())
```

---

## 📁 Project Structure

```
Appointment-Query-Service/
├── app/
│   ├── api/
│   │   └── appointments.py              # GET /appointments
│   ├── db/
│   │   ├── models.py                    # Appointment model
│   │   └── database.py                  # Connection pool
│   ├── schemas/
│   │   └── appointment.py               # Response schemas
│   ├── config.py                        # Settings
│   └── main.py                          # FastAPI app
├── tests/
│   ├── __init__.py
│   └── test_list_appointments.py
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
uvicorn app.main:app --reload --port 8089
pytest tests/ -v
```

---

## 📊 Endpoints

**List Appointments:**
```bash
GET /appointments?user_id=user123&status=scheduled&page=1&limit=20
Authorization: Bearer <jwt_token>
```

**Response (200):**
```json
{
  "total": 45,
  "page": 1,
  "limit": 20,
  "data": [
    {
      "id": "apt-uuid-1",
      "user_id": "user123",
      "service_id": "service456",
      "scheduled_time": "2026-02-15T14:30:00Z",
      "status": "scheduled",
      "created_at": "2026-01-25T10:20:30Z"
    }
  ]
}
```

**Query Parameters:**
- `user_id` - Filter by user
- `status` - Filter by status (scheduled, completed, cancelled)
- `service_id` - Filter by service
- `from_date` - Start date range
- `to_date` - End date range
- `page` - Pagination
- `limit` - Results per page

---

## 📌 Technology Stack

| Component | Technology |
|-----------|-----------|
| Framework | FastAPI |
| DB | PostgreSQL 15 |
| ORM | SQLAlchemy 2.0+ |
| Validation | Pydantic 2.0+ |
| Testing | Pytest |
| Container | Docker & Docker Compose |

---

**v1.0.0** | January 2026
