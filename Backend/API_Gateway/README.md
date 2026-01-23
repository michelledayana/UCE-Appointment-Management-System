# API Gateway

The central entry point for the appointment scheduling microservices ecosystem. This API Gateway implements cross-cutting concerns including authentication, authorization, request routing, and load balancing for all backend services.

## 📋 Project Overview

The API Gateway serves as a **facade** for client applications, providing:
- **Request Routing** – Route client requests to appropriate backend microservices
- **Authentication & Authorization** – JWT-based token validation and role-based access control
- **Cross-Cutting Concerns** – Centralized logging, error handling, and CORS management
- **Service Integration** – HTTP clients for seamless communication with backend domains
- **API Documentation** – Auto-generated OpenAPI/Swagger documentation

---

## 🏗️ Architecture

This API Gateway implements the **Facade Pattern** with **Hexagonal Architecture**, acting as a single entry point for multiple microservices:

```
┌─────────────────────────────────────────────────────────────┐
│                    Client Applications                        │
│         (Web: http://localhost:3000, Mobile, Desktop)        │
└────────────────────────────┬────────────────────────────────┘
                             │
                    ┌────────▼─────────┐
                    │   API Gateway    │
                    │  (Port 8000)     │
                    └─────────┬────────┘
                              │
        ┌─────────────────────┼──────────────────────┬──────────────────┐
        │                     │                      │                  │
    ┌───▼────┐          ┌────▼────┐         ┌──────▼──┐        ┌──────▼───┐
    │  Auth  │          │  Users  │         │Scheduling         │Appointment│
    │Service │          │ Service │         │Service  │        │Service   │
    └────────┘          └────────┘         └─────────┘        └──────────┘
                                                  │
                                          ┌───────┼───────┐
                                          │       │       │
                                      ┌───▼──┐┌──▼───┐┌──▼────┐
                                      │Catalog
                                      │Catalog    │Admin │Query  │
                                      │Service    │Svc   │Svc    │
                                      └────────┘└──────┘└───────┘
```

### Request Flow Through API Gateway

```
Client Request
      │
      ├─→ CORS Middleware (allowed origins check)
      │
      ├─→ Logging Middleware (request logging)
      │
      ├─→ Auth Middleware (JWT validation)
      │     └─→ Public routes bypass auth
      │     └─→ Protected routes require valid token
      │
      ├─→ Role Middleware (RBAC - if needed)
      │
      ├─→ Route Handler
      │     └─→ Service Client (HTTP call to microservice)
      │
      └─→ Response (with standardized format)
```

---

## 🎯 Design Patterns

### 1. **Facade Pattern**
- Single entry point for multiple backend services
- Clients interact with API Gateway, not individual microservices
- Decouples client applications from service topology changes

### 2. **Hexagonal Architecture (Ports & Adapters)**
- **Ports:** API routes, middleware interfaces
- **Adapters:** HTTP service clients, JWT handlers
- Clean separation between business logic and infrastructure

### 3. **Middleware Stack Pattern**
- Request/Response processing pipeline
- Each middleware handles one concern (logging, auth, CORS)
- Composable and reusable middleware

### 4. **Dependency Injection**
- JWT dependencies injected into route handlers
- Service clients injected for testability
- Loose coupling between components

### 5. **Service Integration Pattern**
- Dedicated service clients for each domain
- HTTP/HTTPX-based async communication
- Centralized configuration for service URLs

### 6. **JWT Token-Based Authentication**
- Stateless authentication using JSON Web Tokens
- Token validation via `decode_token()` and `verify_token()`
- Role-based access control (RBAC) via token claims

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Framework** | FastAPI | Modern async web framework |
| **ASGI Server** | Uvicorn | High-performance async server |
| **HTTP Client** | HTTPX & Requests | Async/sync HTTP communication |
| **Authentication** | Python-Jose (JWT) | Token generation & validation |
| **Configuration** | Pydantic Settings | Environment-based configuration |
| **CORS** | FastAPI CORSMiddleware | Cross-origin resource sharing |
| **Testing** | Pytest | Unit and integration testing |
| **Containerization** | Docker & Docker Compose | Service orchestration |
| **Python** | 3.9+ | Runtime |

---

## 📁 Project Structure

```
api-gateway/
├── app/
│   ├── __init__.py
│   ├── main.py                           # FastAPI app + middleware setup
│   ├── config.py                         # Pydantic settings (env vars)
│   │
│   ├── middlewares/
│   │   ├── __init__.py
│   │   ├── auth_middleware.py            # JWT validation middleware
│   │   ├── role_middleware.py            # RBAC middleware (optional)
│   │   └── logging.py                    # Request/response logging
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py                       # Auth endpoints (/auth)
│   │   ├── users.py                      # User management (/users)
│   │   ├── profile.py                    # User profiles (/profiles)
│   │   ├── catalog.py                    # Service catalog (/catalog)
│   │   ├── scheduling.py                 # Scheduling (/scheduling)
│   │   ├── appointment.py                # Appointments (/appointments)
│   │   └── admin.py                      # Admin operations (/admin)
│   │
│   ├── security/
│   │   ├── __init__.py
│   │   ├── jwt_handler.py                # JWT encoding/decoding logic
│   │   └── dependencies.py               # FastAPI dependency injection
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_client.py                # Auth service HTTP client
│   │   ├── user_client.py                # User service HTTP client
│   │   ├── catalog_client.py             # Catalog service HTTP client
│   │   └── appointment_client.py         # Appointment service HTTP client
│   │
│   └── utils/
│       ├── __init__.py
│       ├── http_client.py                # Shared HTTP utilities
│       └── jwt.py                        # JWT utility functions
│
├── tests/
│   ├── __init__.py
│   ├── test_auth_middleware.py          # Auth middleware tests
│   └── test_role_middleware.py          # RBAC tests
│
├── .env                                  # Environment variables (git-ignored)
├── .env.example                          # Environment template
├── .gitignore                            # Git ignore rules
├── docker-compose.yml                    # Docker composition
├── Dockerfile                            # Container image
├── requirements.txt                      # Python dependencies
├── run.py                                # Development server runner
├── start.sh                              # Linux/Mac startup script
├── start.bat                             # Windows startup script
├── QUICK_START.md                        # Quick start guide
├── SETUP_INSTRUCTIONS.md                 # Detailed setup for Windows
└── README.md                             # This file
```

---

## 🔑 Key Components

### **1. Main Application (`app/main.py`)**

FastAPI application with integrated middleware stack:

```python
# CORS Configuration
- Allows requests from http://localhost:3000
- Supports credentials (cookies, auth headers)
- Allows all HTTP methods and headers

# Middleware Stack (in order)
1. CORSMiddleware – Handle cross-origin requests
2. Logging Middleware – Log all requests/responses
3. Auth Middleware – Validate JWT tokens

# Routers (7 domains)
- /auth – Authentication operations
- /users – User management
- /profiles – User profile operations
- /catalog – Service catalog
- /scheduling – Scheduling operations
- /appointments – Appointment management
- /admin – Admin operations

# Health Endpoint
GET /health → { "status": "healthy" }
```

### **2. Authentication Middleware (`app/middlewares/auth_middleware.py`)**

Centralized JWT token validation:

```python
# Public Routes (bypass authentication)
- /auth/login
- /users/register
- /health
- /docs, /redoc, /openapi.json (Swagger UI)

# Protected Routes
- All other routes require "Authorization: Bearer <token>" header
- Token validation via JWT decode
- User payload attached to request.state.user
- Invalid tokens return 401 Unauthorized
```

### **3. JWT Handler (`app/security/jwt_handler.py`)**

Token encoding and decoding utilities:

```python
def decode_token(token: str) -> Optional[Dict]
  └─ Decodes JWT without exceptions
  └─ Returns None if invalid

def verify_token(token: str) -> Dict
  └─ Decodes JWT with exception handling
  └─ Raises Exception if invalid
  └─ Returns payload with user claims
```

### **4. Service Clients (`app/services/`)**

HTTP clients for backend service integration:

- **auth_client.py** – Login and authentication operations
- **user_client.py** – User registration and management
- **catalog_client.py** – Service catalog queries
- **appointment_client.py** – Appointment CRUD operations

Each client:
- Uses async HTTPX for non-blocking requests
- Integrates with configured service URLs from `.env`
- Handles response parsing and error propagation

### **5. Configuration (`app/config.py`)**

Environment-based settings using Pydantic:

```python
# JWT Configuration
- JWT_SECRET – Secret key for token signing (REQUIRED)
- JWT_ALGORITHM – Algorithm (default: HS256)
- JWT_EXPIRE_MINUTES – Token TTL (default: 60)

# Microservice URLs (all REQUIRED)
User Domain:
  - USER_REGISTRATION_URL
  - AUTH_SERVICE_URL
  - USER_PROFILE_URL

Service Domain:
  - SERVICE_CATALOG_URL

Scheduling Domain:
  - SCHEDULING_MANAGEMENT_URL
  - AVAILABILITY_SERVICE_URL

Appointment Domain:
  - APPOINTMENT_CREATION_URL
  - APPOINTMENT_MANAGEMENT_URL
  - APPOINTMENT_QUERY_URL

Admin Domain:
  - ADMINISTRATION_SERVICE_URL
```

### **6. Dependencies (`app/security/dependencies.py`)**

Dependency injection for route handlers:

```python
def admin_required(authorization: str = Header(...))
  └─ Validates token has role="ADMIN"
  └─ Returns admin user payload
  └─ Raises 403 Forbidden if not admin

# Usage in routes:
@router.post("/admin/action")
def admin_action(admin: dict = Depends(admin_required)):
    # Only accessible to admin users
    pass
```

---

## 🚀 Setup & Installation

### Prerequisites

- Python 3.9+
- Docker & Docker Compose (recommended)
- Backend microservices running (or configured in `.env`)

### Option 1: Docker Compose (Recommended)

```bash
# Build and start API Gateway
docker-compose up -d

# Verify it's running
curl http://localhost:8000/health

# View interactive API docs
# Open: http://localhost:8000/docs

# Stop services
docker-compose down
```

### Option 2: Local Development

#### Windows (PowerShell)

```powershell
# 1. Activate virtual environment
..\..\.venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file
cp .env.example .env
notepad .env  # Edit with actual service URLs

# 4. Run the gateway
python run.py
```

#### Linux/Mac

```bash
# 1. Activate virtual environment
source ../../../venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file
cp .env.example .env
nano .env  # Edit with actual service URLs

# 4. Run the gateway
python run.py
```

### Environment Variables

Create a `.env` file in the project root:

```env
# ==================== JWT ====================
JWT_SECRET=your-super-secret-key-change-this
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60

# ================ USER DOMAIN ================
USER_REGISTRATION_URL=http://localhost:8081
AUTH_SERVICE_URL=http://localhost:8082
USER_PROFILE_URL=http://localhost:8083

# =============== SERVICE DOMAIN ==============
SERVICE_CATALOG_URL=http://localhost:8084

# ============== SCHEDULING DOMAIN ============
SCHEDULING_MANAGEMENT_URL=http://localhost:8085
AVAILABILITY_SERVICE_URL=http://localhost:8086

# ============= APPOINTMENT DOMAIN ============
APPOINTMENT_CREATION_URL=http://localhost:8087
APPOINTMENT_MANAGEMENT_URL=http://localhost:8088
APPOINTMENT_QUERY_URL=http://localhost:8089

# =============== ADMIN DOMAIN ================
ADMINISTRATION_SERVICE_URL=http://localhost:8090
```

---

## 📚 API Endpoints

### Authentication

```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}

Response: 200 OK
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

### User Management

```http
POST /users/register
Content-Type: application/json

{
  "email": "newuser@example.com",
  "password": "securepass",
  "firstName": "John",
  "lastName": "Doe"
}

GET /profiles/{userId}
Authorization: Bearer <token>

Response: 200 OK
{
  "id": "user123",
  "email": "user@example.com",
  "firstName": "John",
  "lastName": "Doe",
  "role": "USER"
}
```

### Appointments

```http
GET /appointments?limit=10&offset=0
Authorization: Bearer <token>

POST /appointments
Authorization: Bearer <token>
Content-Type: application/json

{
  "serviceId": "service123",
  "availabilitySlotId": "slot456",
  "notes": "Check-up appointment"
}
```

### Health Check

```http
GET /health

Response: 200 OK
{
  "status": "healthy"
}
```

---

## 🧪 Testing

### Run All Tests

```bash
pytest -v --tb=short
```

### Run Specific Test Suite

```bash
# Test authentication middleware
pytest tests/test_auth_middleware.py -v

# Test RBAC middleware
pytest tests/test_role_middleware.py -v
```

### Test with Coverage

```bash
pip install pytest-cov
pytest --cov=app --cov-report=html
open htmlcov/index.html  # View coverage report
```

### Test Authentication

```bash
# 1. Get a valid token
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"password123"}'

# 2. Use token to access protected endpoint
curl http://localhost:8000/profiles/123 \
  -H "Authorization: Bearer <token_from_step_1>"
```

---

## 🔒 Security Features

### 1. **JWT Token Validation**
- Every protected request is validated via JWT
- Token expiration enforced (default: 60 minutes)
- Invalid tokens return 401 Unauthorized

### 2. **Role-Based Access Control (RBAC)**
- Tokens contain role claims (USER, ADMIN, etc.)
- `admin_required()` dependency enforces admin-only access
- Tokens must include `"role": "ADMIN"` claim

### 3. **CORS Protection**
- Restricts requests to whitelisted origins
- Frontend origin whitelist: `http://localhost:3000`
- Only specific origins can access API

### 4. **Public Routes Whitelist**
Auth bypass only for:
- `/auth/login` – Public authentication
- `/users/register` – Public user registration
- `/health` – Health checks
- `/docs`, `/redoc`, `/openapi.json` – Swagger UI

### 5. **Secure Configuration**
- JWT_SECRET stored in environment (never in code)
- Service URLs externalized (not hardcoded)
- Sensitive values use Pydantic validation

---

## 🔄 Service Integration Flow

```
Client Request
    ↓
API Gateway (Port 8000)
    ├─ /auth/login → calls AUTH_SERVICE_URL
    ├─ /users/register → calls USER_REGISTRATION_URL
    ├─ /profiles/* → calls USER_PROFILE_URL
    ├─ /appointments/* → routes to APPOINTMENT_*_URL based on operation
    ├─ /scheduling/* → calls SCHEDULING_MANAGEMENT_URL
    ├─ /catalog/* → calls SERVICE_CATALOG_URL
    └─ /admin/* → calls ADMINISTRATION_SERVICE_URL
    ↓
Backend Microservices (various ports: 8081-8090)
    ↓
Response → Client (with standardized format)
```

---

## 🐛 Troubleshooting

### ❌ "JWT_SECRET is required"

**Problem:** Missing environment variables in `.env`

```bash
# Solution: Create .env file
cp .env.example .env
# Edit with actual values
```

### ❌ "Connection refused" (127.0.0.1:8081)

**Problem:** Backend microservices not running

```bash
# Solution: Verify backend services are running
curl http://localhost:8081/health  # Check USER_REGISTRATION_URL
curl http://localhost:8082/health  # Check AUTH_SERVICE_URL
# etc.
```

### ❌ "Address already in use" (Port 8000)

**Problem:** Another process is using port 8000

```powershell
# Windows: Find and kill process
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -i :8000
kill -9 <PID>
```

### ❌ "Module not found: fastapi"

**Problem:** Dependencies not installed

```bash
# Solution:
pip install -r requirements.txt
```

### ❌ "Invalid token" (401 Unauthorized)

**Problem:** Token missing or malformed

```bash
# Solution: Include Authorization header correctly
curl http://localhost:8000/appointments \
  -H "Authorization: Bearer <valid_token>"

# Not valid:
-H "Authorization: <token>"          # Missing "Bearer "
-H "Authorization: Bearer invalid"   # Invalid token
```

### ❌ CORS Error in Browser

**Problem:** Frontend origin not whitelisted

```python
# Solution: Update CORS origins in app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Add frontend URL here
        "https://yourfrontend.com"
    ],
    # ...
)
```

---

## 📊 Monitoring & Logging

### View API Documentation

```
http://localhost:8000/docs        # Interactive Swagger UI
http://localhost:8000/redoc       # ReDoc (alternative UI)
http://localhost:8000/openapi.json # OpenAPI schema (JSON)
```

### View Request Logs

Logging middleware automatically logs:
- Request method, path, query parameters
- Response status code, execution time
- Request/response headers (sanitized)

Output appears in terminal where `python run.py` is running.

### Monitor Service Health

```bash
# Health check endpoint
curl http://localhost:8000/health

# Detailed health (if implemented in each service)
curl http://localhost:8000/auth/health
curl http://localhost:8000/users/health
# etc.
```

---

## 🚀 Performance Tips

1. **Use async/await** – All service clients use HTTPX for non-blocking I/O
2. **Connection pooling** – HTTPX automatically pools connections
3. **Uvicorn workers** – Scale with multiple workers:
   ```bash
   uvicorn app.main:app --workers 4 --host 0.0.0.0 --port 8000
   ```
4. **Caching** – Consider caching service responses with Redis
5. **Rate limiting** – Add rate limiting middleware for public endpoints

---

## 🔗 Related Services

This API Gateway integrates with:

| Service | Port | Domain | Purpose |
|---------|------|--------|---------|
| User Registration | 8081 | User | User account creation |
| Auth Service | 8082 | User | JWT token generation |
| User Profile | 8083 | User | User profile management |
| Service Catalog | 8084 | Service | Service offerings |
| Scheduling Mgmt | 8085 | Scheduling | Schedule management |
| Availability | 8086 | Scheduling | Slot availability |
| Appointment Creation | 8087 | Appointment | Create appointments |
| Appointment Mgmt | 8088 | Appointment | Manage appointments |
| Appointment Query | 8089 | Appointment | Query appointments |
| Administration | 8090 | Admin | Audit logs & admin ops |

---