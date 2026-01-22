# API Gateway

Punto de entrada único para todos los microservicios del sistema de programación de citas.

## 🚀 Ejecución Local (Recomendado para Desarrollo)

### 1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

### 2. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con las URLs correctas de los microservicios
```

### 3. Ejecutar:
```bash
python run.py
```

O directamente con uvicorn:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

El API Gateway estará disponible en: `http://localhost:8000`

## 🐳 Ejecución con Docker

```bash
docker-compose up --build
```

## 📋 Endpoints Disponibles

- `GET /health` - Health check
- `POST /auth/login` - Autenticación
- `POST /users/register` - Registro de usuarios
- `GET /profiles/me` - Mi perfil
- `GET /catalog/services` - Listar servicios
- `POST /appointments` - Crear cita
- `GET /appointments/my` - Mis citas
- `GET /admin/*` - Endpoints de administración

## 🔐 Variables de Entorno Requeridas

Ver `.env.example` para la lista completa de variables necesarias.

## 📚 Documentación

Una vez corriendo, accede a:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
