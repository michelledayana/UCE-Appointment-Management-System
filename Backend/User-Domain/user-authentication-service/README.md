# User Authentication Service

## 📋 Description
Service responsible for **user authentication and JWT token generation**. Validates credentials, manages login sessions, and issues secure JWT tokens. Integrates with PostgreSQL for user records and Kafka for publishing authentication events.

---

## 🏗️ Architecture Used

**Layered Architecture + JWT Token Management**

```
┌──────────────────────────────────────────────────┐
│         Authentication API                       │
│         (POST /login, POST /verify)              │
└────────────────┬─────────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────────┐
│         Auth Service Layer                       │
│         - Credential validation                  │
│         - JWT generation                         │
│         - Token verification                     │
└────────────────┬─────────────────────────────────┘
                 │
       ┌─────────┴──────────┬──────────┐
       │                    │          │
  ┌────▼────┐         ┌────▼──┐   ┌──▼────┐
  │PostgreSQL│        │Kafka  │   │ JWT   │
  │ (Users) │        │(Events)│   │(Sign) │
  └──────────┘        └───────┘   └───────┘
```

**Why This Architecture:**
- ✅ **Layered**: Clear separation of auth concerns
- ✅ **JWT**: Stateless token-based authentication
- ✅ **PostgreSQL**: Persistent user records
- ✅ **Kafka**: Audit trail of auth events

---

## 🎯 Design Principles

| Principle | Application | Benefit |
|-----------|---|---|
| **Stateless Auth** | JWT tokens | Horizontally scalable |
| **Password Hashing** | bcrypt + salt | Secure credential storage |
| **Token Expiration** | Short-lived JWTs | Reduces token hijacking risk |
| **Refresh Tokens** | Separate long-lived tokens | Better security/UX balance |
| **Event Logging** | Kafka audit events | Security compliance |

---

## 💾 Database

**PostgreSQL 15** (User Credentials)

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for fast lookups
CREATE INDEX idx_email ON users(email);
CREATE INDEX idx_is_active ON users(is_active);
```

**Why PostgreSQL:**
- Strong ACID for user account integrity
- Unique constraints on email
- Audit trail with timestamps

---

## 🔒 Security

```
┌──────────────────────────────────────────┐
│    Client (Frontend) Login Form          │
└────────────┬─────────────────────────────┘
             │ HTTPS/TLS 1.3
             ▼
┌──────────────────────────────────────────┐
│  Auth Service (Password Validation)      │
│  - Verify email exists                   │
│  - bcrypt compare password               │
│  - Check account active                  │
└────────────┬─────────────────────────────┘
             │
             ▼
┌──────────────────────────────────────────┐
│  JWT Token Generation                    │
│  - Sign with SECRET_KEY                  │
│  - Set expiration (15 minutes)           │
│  - Include user claims (sub, role)       │
└────────────┬─────────────────────────────┘
             │
             ▼
┌──────────────────────────────────────────┐
│  Return Token to Client                  │
│  Authorization: Bearer <jwt_token>       │
└──────────────────────────────────────────┘
```

| Component | Technique | Purpose |
|-----------|---------|----------|
| **Password Storage** | bcrypt + salt | Irreversible hashing |
| **JWT Signing** | HS256 algorithm | Tamper-proof tokens |
| **Token Expiration** | 15-min access, 7-day refresh | Time-limited access |
| **Secure Headers** | HttpOnly, Secure flags | Prevent XSS token theft |
| **Rate Limiting** | 5 failed attempts = block | Prevent brute force |
| **HTTPS/TLS** | TLS 1.3 encryption | Protect credentials in transit |
| **CORS** | Cloudflare + WAF | Prevent unauthorized origin calls |
| **Input Validation** | Pydantic email validation | Sanitize input |

---

## 🧪 Testing

**Test Suite:**
```bash
pytest tests/ -v --cov=app
```

| Test | Location | Tests |
|------|-----------|-----------|
| **Password Tests** | `test_password.py` | Hashing/validation |
| **JWT Tests** | `test_jwt_handler.py` | Token generation/validation |
| **Login Tests** | `test_login_endpoint.py` | Full auth flow |

**Example:**
```python
def test_login_success(client, test_user):
    response = client.post(
        "/login",
        json={"email": "user@example.com", "password": "secure_password"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
```

---

## 📁 Project Structure

```
user-authentication-service/
├── app/
│   ├── config.py                        # Settings (JWT secret, etc)
│   ├── main.py                          # FastAPI app
│   ├── controllers/
│   │   └── auth_controller.py           # /login, /verify endpoints
│   ├── database/
│   │   └── db.py                        # PostgreSQL connection
│   ├── models/
│   │   └── auth_model.py                # User ORM model
│   ├── schemas/
│   │   └── auth_schema.py               # Pydantic models
│   ├── security/
│   │   ├── jwt_handler.py               # JWT encode/decode
│   │   └── password.py                  # bcrypt hashing
│   └── services/
│       ├── auth_service.py              # Business logic
│       └── kafka_consumer.py            # Listen to user events
├── tests/
│   ├── test_password.py
│   ├── test_jwt_handler.py
│   └── test_login_endpoint.py
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
uvicorn app.main:app --reload --port 8092
pytest tests/ -v
```

---

## 📊 Endpoints

**Login:**
```bash
POST /login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 900
}
```

**Refresh Token:**
```bash
POST /refresh
Authorization: Bearer <refresh_token>
```

**Verify Token:**
```bash
POST /verify
Authorization: Bearer <jwt_token>
```

---

## 📌 Technology Stack

| Component | Technology |
|-----------|-----------|
| Framework | FastAPI |
| DB | PostgreSQL 15 |
| Password Hashing | bcrypt |
| JWT | PyJWT |
| Validation | Pydantic |
| Testing | Pytest |
| Container | Docker & Docker Compose |

---

## 🔐 JWT Token Format

```
Header:
{
  "alg": "HS256",
  "typ": "JWT"
}

Payload:
{
  "sub": "user-uuid",        // Subject (user ID)
  "email": "user@example.com",
  "role": "user",
  "iat": 1704891000,         // Issued at
  "exp": 1704891900          // Expiration (15 min)
}
```

