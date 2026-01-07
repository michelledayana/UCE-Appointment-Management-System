from sqlalchemy import create_engine  # <--- REMUEVE 'create_all' de aquí
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL

# Crear el motor de conexión
engine = create_engine(DATABASE_URL)

# Crear la fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

# Función para crear las tablas (esto es lo que usa create_all correctamente)
def init_db():
    Base.metadata.create_all(bind=engine)