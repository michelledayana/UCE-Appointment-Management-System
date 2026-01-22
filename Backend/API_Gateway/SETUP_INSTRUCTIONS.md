# Instrucciones de Configuración - API Gateway

## 🚀 Para Windows (PowerShell)

### Paso 1: Activar Entorno Virtual
```powershell
cd "C:\Users\Michelle Heredia\Desktop\appointment scheduling project 2\Backend\API_Gateway"
..\..\.venv\Scripts\Activate.ps1
```

### Paso 2: Instalar Dependencias
```powershell
pip install -r requirements.txt
```

**⚠️ NOTA:** Asegúrate de escribir `requirements.txt` completo (no `requirements.t`)

### Paso 3: Crear Archivo .env
```powershell
# Si existe .env.example, copiarlo
Copy-Item .env.example .env

# Editar .env con las URLs correctas de tus microservicios
notepad .env
```

### Paso 4: Ejecutar API Gateway
```powershell
python run.py
```

O usar el script automatizado:
```powershell
.\start.bat
```

## ✅ Verificar que Funciona

Abre una nueva terminal PowerShell y ejecuta:
```powershell
curl http://localhost:8000/health
```

O abre en el navegador:
```
http://localhost:8000/docs
```

## 📋 Checklist de Variables .env

Asegúrate de que tu `.env` tenga estas variables:

```env
# JWT (OBLIGATORIO)
JWT_SECRET=tu-secret-key-aqui
JWT_ALGORITHM=HS256

# URLs de Microservicios (ajustar según tus puertos)
USER_REGISTRATION_URL=http://localhost:8081
AUTH_SERVICE_URL=http://localhost:8082
USER_PROFILE_URL=http://localhost:8083
SERVICE_CATALOG_URL=http://localhost:8084
# ... etc
```

## 🐛 Problemas Comunes

### Error: "requirements.txt not found"
- Verifica que estés en el directorio correcto: `Backend/API_Gateway`
- El archivo debe llamarse exactamente `requirements.txt` (no `requirements.t`)

### Error: "JWT_SECRET is required"
- Crea el archivo `.env` con todas las variables necesarias
- Usa `.env.example` como referencia

### Error: "Module not found"
- Instala las dependencias: `pip install -r requirements.txt`
- Verifica que el entorno virtual esté activado

### Error: "Address already in use"
- El puerto 8000 está ocupado
- Cierra la aplicación que lo está usando o cambia el puerto en `run.py`

## 📝 Comandos Útiles

```powershell
# Ver qué está corriendo en el puerto 8000
netstat -ano | findstr :8000

# Matar proceso en puerto 8000 (reemplazar <PID> con el número)
taskkill /PID <PID> /F

# Ver logs si algo falla
python run.py
```
