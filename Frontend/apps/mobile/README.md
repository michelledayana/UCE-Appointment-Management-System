# Sistema de Agendamiento de Citas - Aplicación Móvil Flutter

Aplicación móvil desarrollada en Flutter para el sistema de agendamiento de citas.

## 🚀 Características

- ✅ Autenticación (Login/Registro)
- ✅ Listado de servicios
- ✅ Agendamiento de citas
- ✅ Visualización de citas agendadas
- ✅ Almacenamiento seguro de tokens JWT
- ✅ Material Design

## 📋 Requisitos

- Flutter SDK 3.0.0 o superior
- Dart 3.0.0 o superior
- Android Studio / VS Code con extensiones de Flutter

## 🛠️ Instalación

1. **Instalar dependencias:**
```bash
flutter pub get
```

2. **Configurar API URL:**
El URL del API Gateway está configurado en `lib/config/api_config.dart`:
```dart
static const String baseUrl = 'http://10.0.1.245:8000';
```

## ▶️ Ejecutar

```bash
# Android
flutter run

# iOS
flutter run -d ios

# Web (si está habilitado)
flutter run -d chrome
```

## 📱 Funcionalidades

### Autenticación
- Login con email y contraseña
- Registro de nuevos usuarios
- Validaciones de formularios
- Almacenamiento seguro de tokens

### Servicios
- Listado de servicios disponibles
- Información detallada de cada servicio
- Navegación a agendamiento

### Citas
- Selección de fecha y hora
- Creación de citas
- Visualización de citas agendadas
- Estados de citas (Programada, Completada, Cancelada)

## 🔒 Seguridad

- Tokens JWT almacenados con `flutter_secure_storage`
- Headers de autorización automáticos
- Validación de sesión al iniciar la app

## 📁 Estructura del Proyecto

```
lib/
├── config/
│   └── api_config.dart          # Configuración de API
├── models/
│   ├── auth_model.dart          # Modelos de autenticación
│   ├── service_model.dart       # Modelos de servicios
│   └── appointment_model.dart   # Modelos de citas
├── services/
│   ├── auth_service.dart        # Servicio de autenticación
│   ├── catalog_service.dart     # Servicio de catálogo
│   ├── appointment_service.dart # Servicio de citas
│   └── storage_service.dart     # Servicio de almacenamiento
└── screens/
    ├── login_screen.dart         # Pantalla de login
    ├── register_screen.dart     # Pantalla de registro
    ├── home_screen.dart         # Pantalla principal
    ├── services_screen.dart     # Pantalla de servicios
    └── create_appointment_screen.dart # Pantalla de agendamiento
```

## 🔧 Tecnologías Utilizadas

- **Flutter**: Framework de desarrollo
- **http**: Cliente HTTP para peticiones REST
- **flutter_secure_storage**: Almacenamiento seguro de tokens
- **intl**: Formateo de fechas y números

## 📝 Notas

- La aplicación usa `setState` para manejo de estado (sin Bloc/Riverpod/Provider)
- Todas las peticiones incluyen el token JWT en los headers cuando es necesario
- El diseño sigue Material Design guidelines
