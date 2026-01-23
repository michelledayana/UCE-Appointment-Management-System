# User Profile Service

## 📋 Description
Service responsible for **managing user profiles and personal information**. Provides endpoints to retrieve, update, and manage user profile data. Consumes Kafka events from registration and authentication services to keep profiles synchronized.

---

## 🏗️ Architecture Used

**Layered Architecture + Event Consumer**

```
┌──────────────────────────────────────────────────┐
│         Profile API                              │
│         (GET/PUT /profile)                       │
└────────────────┬─────────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────────┐
│         Profile Service Layer                    │
│         - User data retrieval                    │
│         - Profile updates                        │
│         - Event consumption                      │
└────────────────┬─────────────────────────────────┘
                 │
       ┌─────────┴──────────┬──────────┐
       │                    │          │
  ┌────▼────┐         ┌────▼──┐      │
  │PostgreSQL│        │Kafka  │      │
  │ (Profiles)        │Consumer    │
  └──────────┘        └───────┘      │
                                    
```

**Why This Architecture:**
- ✅ **Layered**: Clean separation of concerns
- ✅ **Event-Driven**: Stays in sync with user registration
- ✅ **PostgreSQL**: Normalized user profile data
- ✅ **Kafka Consumer**: Listens to registration events

---

## 🎯 Design Principles

| Principle | Application | Benefit |
|-----------|---|---|
| **Eventual Consistency** | Kafka-driven updates | Eventually syncs with auth service |
| **Repository Pattern** | Data access abstraction | Easy to test and maintain |
| **DTOs** | Separate response models | Control API surface |
| **Event Sourcing** | Consume registration events | Single source of truth in Kafka |
| **Stateless** | No local state | Horizontally scalable |

---

## 💾 Database

**PostgreSQL 15** (User Profiles)

```sql
CREATE TABLE user_profiles (
    id UUID PRIMARY KEY REFERENCES users(id),
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(50),
    postal_code VARCHAR(20),
    country VARCHAR(100),
    avatar_url VARCHAR(255),
    bio TEXT,
    preferences JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for common queries
CREATE INDEX idx_email_profile ON user_profiles(email);
CREATE INDEX idx_user_id ON user_profiles(id);
```

**Why PostgreSQL:**
- JSONB for flexible preferences
- Strong typing for normalized profile fields
- ACID transactions for profile updates

---

## 🔒 Security

| Component | Technique | Purpose |
|-----------|---------|----------|
| **Authentication** | JWT Bearer Token | Validate user making request |
| **Authorization** | User ID matching | Users can only read own profile |
| **Own-Data Rule** | Check request.user_id == profile.id | Prevent unauthorized access |
| **CORS** | Cloudflare protection | Cross-origin security |
| **Input Validation** | Pydantic schemas | Sanitize profile updates |
| **HTTPS/TLS** | Transport encryption | Protect sensitive data |
| **Rate Limiting** | Per-user profile update limits | Prevent abuse |

**Authorization Flow:**
```python
@router.get("/profile")
def get_profile(request: Request, db: Session):
    user_id = request.headers.get("X-User-Id")  # From API Gateway
    profile = db.query(UserProfile).filter(
        UserProfile.id == user_id
    ).first()
    # Only returns user's own profile
    return profile
```

---

## 🧪 Testing

**Test Suite:**
```bash
pytest tests/ -v --cov=app
```

| Test | Location | Tests |
|------|-----------|-----------|
| **Get Profile** | `test_get_profile.py` | Retrieval |
| **Update Profile** | `test_update_profile.py` | Modifications |

**Example:**
```python
def test_get_own_profile(client, auth_headers):
    response = client.get(
        "/profile",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "user@example.com"
```

---

## 📁 Project Structure

```
user-profile-service/
├── app/
│   ├── main.py                          # FastAPI app
│   ├── config/
│   │   └── settings.py                  # Configuration
│   ├── db/
│   │   └── database.py                  # PostgreSQL connection
│   ├── models/
│   │   └── user.py                      # User Profile ORM model
│   ├── routes/
│   │   └── profile.py                   # /profile endpoints
│   ├── schemas/
│   │   └── user.py                      # Pydantic models
│   └── services/
│       └── kafka_consumer.py            # Listen to user.registered events
├── tests/
│   ├── conftest.py
│   ├── test_get_profile.py
│   └── test_update_profile.py
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
uvicorn app.main:app --reload --port 8093
pytest tests/ -v
```

---

## 📊 Endpoints

**Get Profile:**
```bash
GET /profile
Authorization: Bearer <jwt_token>
```

**Response (200):**
```json
{
  "id": "user-uuid",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1-555-0123",
  "address": "123 Main St",
  "city": "San Francisco",
  "state": "CA",
  "postal_code": "94102",
  "country": "USA",
  "avatar_url": "https://avatar.example.com/john.jpg",
  "bio": "Software Engineer",
  "preferences": {"language": "en", "timezone": "PST"}
}
```

**Update Profile:**
```bash
PUT /profile
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "first_name": "Jonathan",
  "phone": "+1-555-0124",
  "preferences": {"language": "es"}
}
```

---

## 📌 Technology Stack

| Component | Technology |
|-----------|-----------|
| Framework | FastAPI |
| DB | PostgreSQL 15 |
| ORM | SQLAlchemy 2.0+ |
| Event Consumer | Kafka |
| Validation | Pydantic |
| Testing | Pytest |
| Container | Docker & Docker Compose |

---

## 🔄 Event Synchronization

**Kafka Events Consumed:**

1. **user.registered** - New user created in registration service
   - Creates initial profile record
   
2. **user.updated** - User info updated in auth service
   - Syncs email and name changes

**Event Listener:**
```python
def consume_user_registered():
    consumer = KafkaConsumer('user.registered')
    for event in consumer:
        user_data = json.loads(event.value)
        # Create profile from event
        create_profile_from_event(user_data)
```

---
