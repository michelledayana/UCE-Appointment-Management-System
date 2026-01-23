# Administration Microservice

A scalable, event-driven microservice for managing system audit logs and administrative operations within the appointment scheduling platform. Built with FastAPI, MongoDB, and Kafka for robust event processing and persistence.

## 📋 Project Overview

The Administration Service is a core component of the microservices ecosystem responsible for:
- **Event Ingestion:** Consuming events from Kafka topics
- **Audit Logging:** Persisting all system events into MongoDB for compliance and analytics
- **Health Monitoring:** Providing service health status endpoints

---

## 🏗️ Architecture & Design Patterns

### Architecture: Hexagonal Architecture (Ports & Adapters)

This service follows **Hexagonal Architecture** principles for separation of concerns and testability:

```
┌──────────────────────────────────────────────────────┐
│            API Layer (FastAPI Routes)                │
│            ├─ REST endpoints (Ports)                 │
│            └─ Health checks                          │
└─────────────────────┬────────────────────────────────┘
                      │
┌─────────────────────▼────────────────────────────────┐
│       Application Layer (Business Logic)             │
│       ├─ Event Handlers (Adapters)                   │
│       ├─ Domain logic & validations                  │
│       └─ Use cases & workflows                       │
└─────────────────────┬────────────────────────────────┘
                      │
┌─────────────────────▼────────────────────────────────┐
│      Infrastructure Layer (Technical Details)        │
│      ├─ MongoDB (Document Store Adapter)             │
│      ├─ Kafka Consumer (Event Streaming Adapter)     │
│      └─ Configuration management                     │
└──────────────────────────────────────────────────────┘
```

**Hexagonal Benefits:**
- 🎯 **Core Independence** – Business logic independent of frameworks
- 🔌 **Plugin Architecture** – Easy to swap MongoDB for another DB
- 🧪 **Testability** – Mock adapters without external dependencies
- 📦 **Separation of Concerns** – Each layer has single responsibility

### Database: MongoDB (NoSQL Document Store)

**Why MongoDB?**
- ✅ **Flexible Schema** – Audit logs with varying event structures
- ✅ **Horizontal Scalability** – Sharding for large audit volumes
- ✅ **Natural JSON Mapping** – Events serialize directly to BSON
- ✅ **TTL Indexes** – Auto-delete old logs based on retention policy

**Collections:**
- `audit_logs` – Stores all system events with full event payload

**Example Document:**
```json
{
  "_id": ObjectId("507f1f77bcf86cd799439011"),
  "event": "appointment.created",
  "source": "appointment-creation-service",
  "timestamp": ISODate("2026-01-22T10:30:00Z"),
  "payload": {
    "appointmentId": "apt-123",
    "userId": "user-456",
    "serviceId": "svc-789"
  },
  "createdAt": ISODate("2026-01-22T10:30:00Z")
}
```

---

## 🎯 Design Patterns Used

### 1. **Event-Driven Architecture**
- 📨 **Asynchronous Processing** – Kafka consumer runs in background
- 🔄 **Eventual Consistency** – Events processed without blocking API
- 🎯 **Decoupled Services** – No direct coupling with event producers
- 💾 **Event Sourcing Friendly** – All system events stored for audit trail

**Example Event Flow:**
```
User Service publishes → [event: "user.created"]
          ↓ (via Kafka)
Administration Service consumes → [event_handlers.py]
          ↓
MongoDb audit_logs collection
```

### 2. **Repository Pattern**
- **Data Access Abstraction** – `database/mongo.py` encapsulates MongoDB queries
- **Centralized Configuration** – Single place for connection pooling and timeouts
- **Testability** – Easy to inject mock MongoDB collections in tests
- **Future-Proof** – Can switch to PostgreSQL without changing business logic

**Example Usage:**
```python
# Dependency injection enables testing
def handle_event(event: dict, collection=None):
    collection = collection or audit_collection  # Default or mock
    collection.insert_one(document)
```

### 3. **Consumer-Based Audit Pattern**
- **Write-Only Operations** – No updates or deletes on audit logs
- **Immutable Records** – Timestamps and event details never change
- **Compliance-Ready** – Meets regulatory requirements (GDPR, HIPAA)
- **Performance Optimized** – Only inserts (fastest MongoDB operation)

### 4. **Dependency Injection (DI)**
- Enables flexible testing without external dependencies
- Constructor or parameter-based injection
- FastAPI's `Depends()` for route-level DI

### 5. **Schema Validation (Pydantic v2)**
- **Type Safety** – All inputs validated before processing
- **Auto Documentation** – Pydantic generates OpenAPI schemas
- **Error Handling** – Clear validation error messages
- **Serialization** – Automatic JSON↔Python object conversion

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Framework** | FastAPI | 
| **ASGI Server** | Uvicorn | 
| **Database** | MongoDB |
| **Message Queue** | Kafka | 
| **ORM/Drivers** | PyMongo | 
| **Validation** | Pydantic | 
| **Environment** | Python-dotenv | 
| **Containerization** | Docker & Docker Compose |
| **Testing** | Pytest | 

---

## 📁 Project Structure

```
administration-service/
├── app/
│   ├── __init__.py                # Package initialization
│   ├── main.py                    # FastAPI application entry point
│   ├── config.py                  # Configuration management (env vars)
│   │
│   ├── api/
│   │   └── rest/
│   │       ├── __init__.py
│   │       └── admin.py          # Admin REST endpoints (health, etc.)
│   │
│   ├── application/
│   │   └── handlers/
│   │       ├── __init__.py
│   │       └── event_handlers.py # Event processing & Kafka consumer logic
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   └── mongo.py              # MongoDB connection & repository pattern
│   │
│   ├── infrastructure/
│   │   └── kafka/
│   │       ├── __init__.py
│   │       └── consumer.py       # Kafka event consumer adapter
│   │
│   └── schemas/
│       ├── __init__.py
│       └── admin_schema.py       # Pydantic models for validation
│
├── docker/
│   └── Dockerfile                # Container image definition
├── tests/
│   ├── __init__.py
│   ├── test_admin_routes.py     # REST endpoint tests
│   ├── test_event_handler.py    # Event handler tests
│   └── test_kafka_processing.py # Kafka consumer tests
│
├── .env                          # Environment variables (create from .env.example)
├── docker-compose.yml            # Multi-container orchestration
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

---

## 🔑 Key Components

### **1. API Layer (`api/rest/admin.py`)**
- **`GET /admin/health`** – Service health status endpoint
- Returns: `{ "service": "administration-service", "status": "ok" }`
- Used for liveness and readiness probes in orchestration

### **2. Event Handler (`application/handlers/event_handlers.py`)**
- **Purpose:** Central event processing logic
- **Function:** `handle_event(event, collection=None)`
  - Receives Kafka events with structure: `{ event, source, payload }`
  - Transforms events into audit documents
  - Persists to MongoDB audit_logs collection
  - Supports dependency injection for testing (mock collections)
- **Key Feature:** Decoupled from Kafka; can be tested independently

### **3. Database Layer (`database/mongo.py`)**
- **MongoDB Connection Manager**
  - Singleton pattern for client reuse
  - Automatic connection pooling
  - Server selection timeout (5000ms)
- **Collections:**
  - `audit_logs` – Stores all system events for compliance and auditing

### **4. Configuration (`config.py`)**
- **Environment Variables (with defaults):**
  - `SERVICE_NAME` → "administration-service"
  - `MONGO_URI` → (Required) MongoDB connection string
  - `MONGO_DB_NAME` → "admin_db" (database name)
  - `KAFKA_BOOTSTRAP_SERVERS` → "kafka:9092" (Kafka brokers)
  - `KAFKA_TOPIC_EVENTS` → "system_events" (topic to consume)

### **5. Kafka Consumer (`infrastructure/kafka/consumer.py`)**
- Listens to configured Kafka topic
- Triggers `handle_event()` for each message
- Implements retry logic and error handling
- Runs as background service

---

## 🚀 Setup & Installation

### Prerequisites
- Docker & Docker Compose (recommended)
- Python 3.9+ (for local development)
- MongoDB and Kafka instances (or use docker-compose)


### Option 2: Local Development

```bash
# Clone and navigate to the service directory
cd Backend/Administration-Domain/Administration-service

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start MongoDB (requires running instance or Docker)
docker run -d -p 27019:27017 mongo:6

# Start Kafka (requires running instance or Docker)
# See the main project's docker-compose for Kafka setup

# Run the service
uvicorn app.main:app --host 0.0.0.0 --port 8090 --reload
```
---

## 🧪 Testing

### Run All Tests
```bash
pytest 
```

### Run Specific Test Suite
```bash
# Test REST endpoints
pytest tests/test_admin_routes.py -v

# Test event handlers
pytest tests/test_event_handler.py -v

# Test Kafka processing
pytest tests/test_kafka_processing.py -v

### Testing Event Handlers (with Dependency Injection)
```python
from tests.conftest import mock_collection
from app.application.handlers.event_handlers import handle_event

def test_event_handler_with_mock():
    mock_collection = MockCollection()
    event = {"event": "user.created", "source": "user-service", "payload": {...}}
    
    handle_event(event, collection=mock_collection)
    
    assert mock_collection.insert_one.called
```

---

## 📊 API Endpoints

### Health Check
```http
GET /admin/health
```

**Response:**
```json
{
  "service": "administration-service",
  "status": "ok"
}
```

---

## 🔄 Event Processing Flow

```
Kafka Topic (system_events)
         ↓
Kafka Consumer (infrastructure/kafka/consumer.py)
         ↓
handle_event() (application/handlers/event_handlers.py)
         ↓
Event Validation (schemas/admin_schema.py with Pydantic)
         ↓
MongoDB Insert (database/mongo.py → audit_logs collection)
         ↓
Audit Log Stored ✓
```

## 📊 Architecture & Database Summary

| Aspect | Administration Service |
|--------|------------------------|
| **Architecture Pattern** | Hexagonal (Ports & Adapters) |
| **Primary Role** | Event Consumer & Auditor |
| **Database Type** | MongoDB (NoSQL Document Store) |
| **Database Access Pattern** | Repository Pattern |
| **Key Design Patterns** | Event-Driven, Repository, Dependency Injection |
| **Consistency Model** | Eventual Consistency |
| **Scalability** | Horizontal (MongoDB sharding) |
| **Data Retention** | TTL-based auto-cleanup |

**Microservice Ecosystem Architecture:**
- **Appointment Creation Service** → Publishes events + writes to PostgreSQL
- **Administration Service** (this) → Consumes & stores in MongoDB for audit
- **Appointment Management Service** → Consumes & maintains read model in PostgreSQL

---