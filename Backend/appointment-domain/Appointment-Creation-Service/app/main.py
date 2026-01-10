import json
import threading
import uvicorn
from fastapi import FastAPI
from kafka import KafkaConsumer
from db.database import engine, Base, SessionLocal
from models.appointment import UserProfile
from routes import profile

# Create database tables for the profile service
Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Profile Service")

# Include the routes for REST API (GET/PUT)
app.include_router(profile.router)

def consume_registration_events():
    """
    Kafka Consumer: Listens to 'user_registered_topic'.
    When a user registers, it creates a basic profile automatically.
    """
    consumer = KafkaConsumer(
        'user_registered_topic',
        bootstrap_servers=['kafka:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='profile-service-group',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

    print("🚀 Kafka Consumer started and listening...")

    for message in consumer:
        user_data = message.value
        db = SessionLocal()
        try:
            # Logic to create the profile with basic data from registration
            new_profile = UserProfile(
                email=user_data['email'],
                full_name=user_data.get('full_name', 'Default Name'),
                user_type=user_data.get('user_type', 'GENERAL'),
                # faculty, career, and phone remain NULL until the user updates them via PUT
            )
            db.add(new_profile)
            db.commit()
            print(f"Profile created automatically for: {user_data['email']}")
        except Exception as e:
            db.rollback()
            print(f"Error creating profile: {e}")
        finally:
            db.close()

# Start Kafka consumer in a background thread so it doesn't block the API
threading.Thread(target=consume_registration_events, daemon=True).start()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8083)