import uvicorn
import threading
from fastapi import FastAPI
from app.controllers.user_controller import router as user_router
from app.database.db import Base, engine 
# Importamos la lógica de Kafka que crearemos
from app.utils.kafka_producer import iniciar_productor 

app = FastAPI(title="User Registration Service")

@app.on_event("startup")
def startup_event():
    print("Verificando y creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas exitosamente.")
    # Opcional: Iniciar validación de Kafka al arrancar
    # iniciar_productor() 

# CAMBIO AQUÍ: Cambiamos el prefijo de /users a /register 
# para que el link sea http://localhost:8081/register/usuario
app.include_router(user_router, prefix="/register", tags=["Users"])

@app.get("/health")
def health():
    return {"status": "UP"}

@app.get("/")
def root():
    return {"service": "User Registration Service"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8081, reload=True)