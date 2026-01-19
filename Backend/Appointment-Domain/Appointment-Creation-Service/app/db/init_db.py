import time
from sqlalchemy import text
from app.db.database import engine, Base
from app.db.models import Appointment


def init_db(retries: int = 5, delay: int = 3):
    for attempt in range(1, retries + 1):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))

            Base.metadata.create_all(bind=engine)
            print("✅ Database connected and tables created")
            return

        except Exception as e:
            print(f"⏳ Database not ready, retrying ({attempt}/{retries})...")
            time.sleep(delay)

    raise Exception("❌ Could not connect to the database")
