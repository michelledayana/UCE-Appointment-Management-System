import uvicorn
from fastapi import FastAPI
from app.controllers.user_controller import router as user_router
from app.database.db import Base, engine  
from app.models.user_model import User 

app = FastAPI(title="User Registration Service")

# 🔹 Crear tablas al iniciar la aplicación
@app.on_event("startup")
def startup_event():
    print("Verificando y creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas exitosamente.")

# ✅ CORRECCIÓN: El prefijo "/register" hará que la ruta sea /register/usuario
app.include_router(user_router, prefix="/register", tags=["Users"])

@app.get("/health")
def health():
    return {"status": "UP"}

@app.get("/")
def root():
    return {"service": "User Registration Service"}

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8081,
        reload=True
    )