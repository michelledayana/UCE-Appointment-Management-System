@echo off
echo ========================================
echo   Iniciando API Gateway
echo ========================================

REM Activar entorno virtual si existe
if exist "..\..\.venv\Scripts\activate.bat" (
    call ..\..\.venv\Scripts\activate.bat
    echo Entorno virtual activado
)

REM Instalar dependencias si es necesario
if not exist ".venv" (
    echo Instalando dependencias...
    pip install -r requirements.txt
)

REM Verificar que existe .env
if not exist ".env" (
    echo.
    echo ⚠️  ADVERTENCIA: Archivo .env no encontrado
    echo Creando desde .env.example...
    if exist ".env.example" (
        copy .env.example .env
        echo ✅ Archivo .env creado. Por favor edítalo con las URLs correctas.
        echo.
        pause
    ) else (
        echo ❌ No se encontró .env.example
        echo Por favor crea manualmente el archivo .env
        pause
        exit /b 1
    )
)

REM Ejecutar API Gateway
echo.
echo Iniciando API Gateway en http://localhost:8000
echo Presiona Ctrl+C para detener
echo.
python run.py

pause
