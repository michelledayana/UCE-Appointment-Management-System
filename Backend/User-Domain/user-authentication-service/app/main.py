import threading
import json
import time
from datetime import datetime, timedelta
from fastapi import FastAPI, APIRouter, HTTPException
from jose import jwt, JWTError  # <--- CORRECCIÓN CLAVE
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

app = FastAPI(title="Servicio de Autenticación")

# --- CONFIGURACIÓN DE SEGURIDAD ---
SECRET_KEY = "clave_secreta_del_proyecto_scheduling" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def crear_token_acceso(data: dict):
    datos_a_cifrar = data.copy()
    expiracion = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    datos_a_cifrar.update({"exp": expiracion})
    # Genera el token usando la librería jose
    return jwt.encode(datos_a_cifrar, SECRET_KEY, algorithm=ALGORITHM)

# --- RUTAS ---
auth_router = APIRouter(prefix="/auth", tags=["Seguridad"])

@auth_router.post("/usuario")
async def registrar_usuario_auth(usuario: dict):
    return {"status": "success", "message": "Ruta /auth/usuario activa"}

@auth_router.post("/login")
async def login_usuario(credenciales: dict):
    email = credenciales.get("email")
    password = credenciales.get("password")

    # Validación manual (luego conectarás a db_auth)
    if email == "dmherediar@uce.edu.ec" and password == "dayanaheredia1234":
        token_real = crear_token_acceso(data={"sub": email})
        return {
            "status": "success",
            "message": "Login exitoso",
            "access_token": token_real,
            "token_type": "bearer"
        }
    else:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

app.include_router(auth_router)

# --- LÓGICA DE KAFKA ---
def conectar_kafka():
    print("--- [LOG] Intentando conectar con Kafka ---")
    while True:
        try:
            consumer = KafkaConsumer(
                'user_registered_topic',
                bootstrap_servers='kafka:9092',
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                group_id='auth-service-group'
            )
            print("--- [LOG] ¡Conectado a Kafka exitosamente! ---")
            return consumer
        except NoBrokersAvailable:
            print("--- [LOG] Kafka no listo. Reintentando... ---")
            time.sleep(5)

def escuchar_eventos():
    consumer = conectar_kafka()
    for message in consumer:
        print(f"--- [LOG] Evento recibido: {message.value} ---")

# Iniciar Kafka en segundo plano
thread = threading.Thread(target=escuchar_eventos, daemon=True)
thread.start()