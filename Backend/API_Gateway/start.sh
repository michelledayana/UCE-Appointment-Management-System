#!/bin/bash

echo "========================================"
echo "  Iniciando API Gateway"
echo "========================================"

# Activar entorno virtual si existe
if [ -d "../../.venv" ]; then
    source ../../.venv/bin/activate
    echo "Entorno virtual activado"
fi

# Instalar dependencias si es necesario
if [ ! -d ".venv" ]; then
    echo "Instalando dependencias..."
    pip install -r requirements.txt
fi

# Verificar que existe .env
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  ADVERTENCIA: Archivo .env no encontrado"
    echo "Creando desde .env.example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ Archivo .env creado. Por favor edítalo con las URLs correctas."
        echo ""
        read -p "Presiona Enter para continuar..."
    else
        echo "❌ No se encontró .env.example"
        echo "Por favor crea manualmente el archivo .env"
        exit 1
    fi
fi

# Ejecutar API Gateway
echo ""
echo "Iniciando API Gateway en http://localhost:8000"
echo "Presiona Ctrl+C para detener"
echo ""
python run.py
