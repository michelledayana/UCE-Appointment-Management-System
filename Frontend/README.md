# Sistema de Programación de Citas - Frontend

Frontend escalable desarrollado con Next.js 14, React, TypeScript y TailwindCSS para el sistema de gestión de citas.

## 🚀 Características

- ✅ Autenticación JWT con roles (ADMIN, USUARIO)
- ✅ Gestión de citas (crear, listar, cancelar)
- ✅ Catálogo de servicios
- ✅ Panel de administración
- ✅ Gestión de perfiles de usuario
- ✅ Diseño responsive (web/móvil)
- ✅ Protección de rutas basada en roles
- ✅ Manejo de errores y estados de carga

## 📋 Requisitos Previos

- Node.js 18+ 
- npm o yarn
- API Gateway corriendo en `http://localhost:8000`

## 🛠️ Instalación

1. **Instalar dependencias:**
```bash
npm install
# o
yarn install
```

2. **Configurar variables de entorno:**
```bash
cp .env.local.example .env.local
```

Editar `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. **Ejecutar en desarrollo:**
```bash
npm run dev
# o
yarn dev
```

4. **Abrir en el navegador:**
```
http://localhost:3000
```

## 📁 Estructura del Proyecto

```
Frontend/
├── app/                    # Páginas y rutas (App Router)
│   ├── login/             # Página de login
│   ├── register/          # Página de registro
│   ├── catalog/           # Catálogo de servicios
│   ├── appointments/       # Gestión de citas
│   ├── profile/           # Perfil de usuario
│   └── admin/             # Panel de administración
├── components/            # Componentes reutilizables
│   ├── common/            # Componentes UI comunes
│   ├── layout/            # Componentes de layout
│   ├── appointments/       # Componentes de citas
│   └── services/          # Componentes de servicios
├── contexts/              # Contextos de React
│   └── AuthContext.tsx    # Contexto de autenticación
├── lib/                   # Utilidades y configuraciones
│   ├── api/               # Servicios API
│   └── axios.ts           # Configuración de Axios
├── types/                 # Tipos TypeScript
└── middleware.ts          # Middleware de Next.js
```

## 🔐 Autenticación

El sistema utiliza JWT (JSON Web Tokens) para la autenticación:

- **Login:** `/login`
- **Registro:** `/register`
- **Logout:** Se maneja automáticamente desde el navbar

Los tokens se almacenan en cookies y se incluyen automáticamente en las peticiones API.

## 🛣️ Rutas

### Públicas
- `/login` - Inicio de sesión
- `/register` - Registro de usuarios

### Protegidas (requieren autenticación)
- `/` - Dashboard principal
- `/catalog` - Catálogo de servicios
- `/appointments` - Mis citas
- `/appointments/new` - Crear nueva cita
- `/profile` - Mi perfil

### Administración (requieren rol ADMIN)
- `/admin` - Panel de administración
- `/admin/services` - Gestión de servicios
- `/admin/services/new` - Crear servicio
- `/admin/appointments` - Todas las citas

## 📡 Integración con API

El frontend se comunica con el API Gateway en `http://localhost:8000`:

### Endpoints principales:
- `POST /auth/login` - Autenticación
- `POST /users/register` - Registro
- `GET /catalog/services` - Listar servicios
- `POST /appointments` - Crear cita
- `GET /appointments/my` - Mis citas
- `GET /profiles/me` - Mi perfil
- `PUT /profiles/me` - Actualizar perfil

## 🎨 Componentes Principales

### Componentes Comunes
- `Button` - Botón reutilizable con variantes
- `Input` - Input con validación
- `Alert` - Alertas de éxito/error
- `Loading` - Indicador de carga

### Componentes de Layout
- `Layout` - Layout principal con protección de rutas
- `Navbar` - Barra de navegación

### Componentes de Dominio
- `AppointmentCard` - Tarjeta de cita
- `ServiceCard` - Tarjeta de servicio

## 🔒 Protección de Rutas

El sistema implementa protección de rutas en dos niveles:

1. **Middleware de Next.js** (`middleware.ts`): Protección a nivel de servidor
2. **Componente Layout**: Protección a nivel de cliente con verificación de roles

## 🧪 Testing

```bash
# Ejecutar linter
npm run lint

# Build de producción
npm run build

# Iniciar en producción
npm start
```

## 📝 Notas de Desarrollo

- El proyecto usa **App Router** de Next.js 14
- Los componentes son **Server Components** por defecto, usa `'use client'` cuando necesites interactividad
- Los estilos usan **TailwindCSS** con clases personalizadas
- La autenticación se maneja con **Context API** de React
- Las peticiones API usan **Axios** con interceptores para tokens

## 🐛 Solución de Problemas

### Error de CORS
Asegúrate de que el API Gateway tenga configurado CORS para `http://localhost:3000`

### Token expirado
El sistema redirige automáticamente a `/login` cuando el token expira

### Error 401
Verifica que el token se esté enviando correctamente en los headers

## 📚 Recursos

- [Next.js Documentation](https://nextjs.org/docs)
- [TailwindCSS](https://tailwindcss.com/docs)
- [React Hook Form](https://react-hook-form.com/)
- [Axios](https://axios-http.com/docs/intro)

## 👥 Contribución

Este es un proyecto académico. Para contribuir:

1. Sigue los principios SOLID y Clean Code
2. Mantén la estructura de carpetas
3. Documenta componentes complejos
4. Usa TypeScript para type safety

---

**Desarrollado para el proyecto académico de Ingeniería de Software**
