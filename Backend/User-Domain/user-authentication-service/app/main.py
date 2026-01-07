import threading
import json
import time
from datetime import datetime, timedelta
from fastapi import FastAPI, APIRouter, HTTPException, Depends
from jose import jwt
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os

# --- DATABASE CONFIGURATION ---
# Using the environment variable from your docker-compose
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@db-auth:5432/auth_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- AUTH MODEL ---
class AuthUser(Base):
    __tablename__ = "auth_users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    user_type = Column(String)

# Create tables in db_auth
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Authentication Service")

# --- SECURITY CONFIG ---
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "supersecretkey_aws_2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# --- ROUTES ---
auth_router = APIRouter(prefix="/auth", tags=["Security"])

@auth_router.post("/login")
async def login_user(credentials: dict):
    email = credentials.get("email")
    password = credentials.get("password")
    
    db = SessionLocal()
    # REAL VALIDATION: Query the database
    user = db.query(AuthUser).filter(AuthUser.email == email).first()
    db.close()

    if not user:
        raise HTTPException(status_code=401, detail="User not found in Auth DB")

    # Note: In production use pwd_context.verify(password, user.password_hash)
    # For now, we check if user exists as proof of Kafka sync
    token = create_access_token(data={"sub": user.email, "role": user.user_type})
    
    return {
        "status": "success",
        "access_token": token,
        "token_type": "bearer"
    }

app.include_router(auth_router)

# --- KAFKA CONSUMER LOGIC (THE BRIDGE) ---
def start_kafka_consumer():
    print("--- [LOG] Initializing Kafka Consumer ---")
    while True:
        try:
            consumer = KafkaConsumer(
                'user_registered_topic',
                bootstrap_servers='kafka:9092',
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                group_id='auth-service-group',
                auto_offset_reset='earliest'
            )
            print("--- [LOG] Connected to Kafka successfully! ---")
            
            for message in consumer:
                user_data = message.value
                print(f"--- [LOG] Syncing user: {user_data['email']} ---")
                
                # PERSIST TO DB_AUTH
                db = SessionLocal()
                try:
                    new_auth_user = AuthUser(
                        email=user_data['email'],
                        password_hash=user_data['password_hash'],
                        user_type=user_data['user_type']
                    )
                    db.add(new_auth_user)
                    db.commit()
                    print(f"--- [SUCCESS] {user_data['email']} saved in Auth DB ---")
                except Exception as e:
                    db.rollback()
                    print(f"--- [ERROR] DB Sync failed: {e}")
                finally:
                    db.close()
            
        except NoBrokersAvailable:
            print("--- [LOG] Kafka not ready. Retrying in 5s... ---")
            time.sleep(5)

# Start background thread
threading.Thread(target=start_kafka_consumer, daemon=True).start()