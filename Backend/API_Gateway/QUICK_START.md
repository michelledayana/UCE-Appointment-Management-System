# Quick Start - API Gateway

## 🚀 Inicio Rápido (Local)

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Crear archivo .env
cp .env.example .env
# Editar .env con las URLs de tus microservicios

# 3. Ejecutar
python run.py
```

## 🔍 Verificar que Funciona

Abre en el navegador: `http://localhost:8000/docs`

O con curl:
```bash
curl http://localhost:8000/health
```

## ⚠️ Problemas Comunes

### "Module not found"
```bash
pip install -r requirements.txt
```

### "JWT_SECRET is required"
Crea el archivo `.env` con todas las variables de `.env.example`

### "Connection refused"
Verifica que los microservicios estén corriendo en los puertos configurados
