# User Registration Service

## 📋 Description
Service responsible for **user registration and account creation**. Validates user information, stores credentials securely in PostgreSQL, and publishes registration events via Kafka for other services to subscribe and react. Implements complete sign-up workflow with email validation.

---

## 🏗️ Architecture Used

**Layered Architecture + Event Publisher**

```
┌──────────────────────────────────────────────────┐
│         Registration API                         │
│         (POST /register)                         │
└────────────────┬─────────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────────┐
│         Registration Service Layer               │
│         - User data validation                   │
│         - Email verification                     │
│         - Password hashing                       │
└────────────────┬─────────────────────────────────┘
                 │
       ┌─────────┴──────────┬──────────┐
       │                    │          │
  ┌────▼────┐         ┌────▼──┐   ┌──▼────┐
  │PostgreSQL│        │Kafka  │   │ Email │
  │(Users)   │        │(Events)   │Server │
  └──────────┘        └───────┘   └───────┘
```

**Why This Architecture:**
- ✅ **Layered**: Clear separation (API → Service → DB)
- ✅ **Event-Driven**: Publish `user.registered` for profile service
- ✅ **PostgreSQL**: Persistent user storage
- ✅ **Kafka**: Asynchronous event propagation

---

## 🎯 Design Principles

| Principle | Application | Benefit |
|-----------|---|---|
| **Validation First** | Multiple validation layers | Prevent invalid data |
| **Password Security** | bcrypt hashing before storage | Never store plain passwords |
| **Event Publishing** | Kafka for user.registered | Decouples from downstream |
| **Idempotency** | Email unique constraint | Prevent duplicate accounts |
| **Audit Trail** | Timestamps on creation | Track account lifecycle |

---

## 💾 Database

**PostgreSQL 15** (User Accounts)

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT FALSE,  -- Require email confirmation
    email_verified BOOLEAN DEFAULT FALSE,
    verification_token VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_email_user ON users(email);
CREATE INDEX idx_is_active ON users(is_active);
CREATE UNIQUE INDEX idx_verification_token ON users(verification_token) 
    WHERE verification_token IS NOT NULL;
```

**Why PostgreSQL:**
- UNIQUE constraint prevents duplicate emails
- ACID transactions for atomic registration
- Verification token tracking for email confirmation

---

## 🔒 Security

```
┌──────────────────────────────────────────┐
│    Frontend Registration Form            │
│    - Email validation (client-side)      │
└────────────┬─────────────────────────────┘
             │ HTTPS/TLS 1.3
             ▼
┌──────────────────────────────────────────┐
│  Registration Service                    │
│  1. Validate email format                │
│  2. Check email not already registered   │
│  3. Hash password (bcrypt)               │
│  4. Validate password strength           │
│  5. Store user record                    │
│  6. Generate verification token         │
│  7. Send verification email             │
└────────────┬─────────────────────────────┘
             │
             ▼
┌──────────────────────────────────────────┐
│  Publish Kafka Event (user.registered)   │
│  - Profile Service consumes             │
│  - Notification Service consumes        │
└──────────────────────────────────────────┘
```

| Component | Technique | Purpose |
|-----------|---------|----------|
| **Password Hashing** | bcrypt + salt | Irreversible storage |
| **Password Validation** | Regex + length checks | Enforce strong passwords |
| **Email Validation** | Format verification + unique constraint | Valid unique email |
| **HTTPS/TLS** | Transport encryption | Protect credentials |
| **CORS** | Cloudflare firewall | Prevent cross-origin abuse |
| **Rate Limiting** | 5 reg attempts/IP/hour | Prevent registration spam |
| **Email Verification** | Token sent to email | Confirm email ownership |
| **Input Sanitization** | Pydantic validators | Prevent injection attacks |
| **CSRF Token** | Token in signup form | Prevent form hijacking |

---

## 🧪 Testing

**Test Suite:**
```bash
pytest tests/ -v --cov=app
```

| Test | Location | Tests |
|------|-----------|-----------|
| **Registration** | `test_register_user_endpoint.py` | Full signup flow |

**Example:**
```python
def test_register_success(client, db):
    response = client.post(
        "/register",
        json={
            "email": "newuser@example.com",
            "password": "SecurePass123!",
            "first_name": "John",
            "last_name": "Doe"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["is_active"] == False  # Not active until verified
    
    # Verify user created in DB
    user = db.query(User).filter(User.email == "newuser@example.com").first()
    assert user is not None
    assert user.password_hash != "SecurePass123!"  # Hashed
```

---

## 📁 Project Structure

```
user-registration-service/
├── app/
│   ├── config.py                        # Settings (SMTP, Kafka, etc)
│   ├── main.py                          # FastAPI app + DB init
│   ├── controllers/
│   │   └── user_controller.py           # /register, /verify endpoints
│   ├── core/
│   │   ├── logger.py                    # Logging setup
│   │   └── security.py                  # Crypto functions
│   ├── database/
│   │   ├── db.py                        # SQLAlchemy setup
│   │   └── dependencies.py              # FastAPI dependencies
│   ├── models/
│   │   └── user_model.py                # User ORM model
│   ├── messaging/
│   │   └── kafka_producer.py            # Publish user.registered event
│   ├── repositories/
│   │   └── user_repository.py           # Data access layer
│   ├── schemas/
│   │   └── user_schema.py               # Pydantic models
│   └── services/
│       └── user_service.py              # Business logic + validation
├── tests/
│   └── test_register_user_endpoint.py
├── database/
│   └── schema.sql                       # Initial schema
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
pytest tests/ -v
```

---

## 📊 Endpoints

**Register User:**
```bash
POST /register
Content-Type: application/json

{
  "email": "newuser@example.com",
  "password": "SecurePassword123!",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response (201):**
```json
{
  "id": "user-uuid",
  "email": "newuser@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "is_active": false,
  "email_verified": false,
  "created_at": "2026-01-25T10:20:30Z"
}
```

**Verify Email:**
```bash
POST /verify
Content-Type: application/json

{
  "token": "verification_token_from_email"
}
```

**Response (200):**
```json
{
  "message": "Email verified successfully",
  "is_active": true
}
```

---

## 📌 Technology Stack

| Component | Technology |
|-----------|-----------|
| Framework | FastAPI |
| DB | PostgreSQL 15 |
| Password Hashing | bcrypt |
| Event Publisher | Kafka |
| Email Service | SMTP |
| Validation | Pydantic |
| Testing | Pytest |
| Container | Docker & Docker Compose |

---

## 🔄 Event Publishing

**Kafka Event (user.registered):**
```json
{
  "event_type": "user.registered",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "newuser@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "created_at": "2026-01-25T10:20:30Z"
}
```

**Consumers:**
- **Profile Service**: Creates user profile record
- **Notification Service**: Sends welcome email
- **Analytics Service**: Tracks registrations

---

## 🔐 Password Requirements

- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character (!@#$%^&*)
