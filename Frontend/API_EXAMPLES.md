# Ejemplos de Uso de la API

Este documento contiene ejemplos de cómo usar los servicios API en el frontend.

## Autenticación

### Login
```typescript
import { authService } from '@/lib/api/auth'

try {
  const response = await authService.login({
    email: 'usuario@example.com',
    password: 'password123'
  })
  // El token se guarda automáticamente en cookies
  console.log('Login exitoso:', response)
} catch (error) {
  console.error('Error en login:', error)
}
```

### Registro
```typescript
import { authService } from '@/lib/api/auth'

try {
  const response = await authService.register({
    full_name: 'Juan Pérez',
    email: 'juan@example.com',
    password: 'password123'
  })
  console.log('Registro exitoso:', response)
} catch (error) {
  console.error('Error en registro:', error)
}
```

## Citas (Appointments)

### Crear Cita
```typescript
import { appointmentService } from '@/lib/api/appointments'

try {
  const appointment = await appointmentService.create({
    user_email: 'usuario@example.com',
    service_name: 'Consulta Médica',
    appointment_date: '2024-01-15T10:00:00Z'
  })
  console.log('Cita creada:', appointment)
} catch (error) {
  console.error('Error al crear cita:', error)
}
```

### Obtener Mis Citas
```typescript
import { appointmentService } from '@/lib/api/appointments'

try {
  const appointments = await appointmentService.getMyAppointments()
  console.log('Mis citas:', appointments)
} catch (error) {
  console.error('Error al obtener citas:', error)
}
```

### Cancelar Cita
```typescript
import { appointmentService } from '@/lib/api/appointments'

try {
  const cancelled = await appointmentService.cancel('appointment-id')
  console.log('Cita cancelada:', cancelled)
} catch (error) {
  console.error('Error al cancelar cita:', error)
}
```

## Catálogo de Servicios

### Listar Servicios
```typescript
import { catalogService } from '@/lib/api/catalog'

try {
  const services = await catalogService.list()
  console.log('Servicios:', services)
} catch (error) {
  console.error('Error al obtener servicios:', error)
}
```

### Crear Servicio (Admin)
```typescript
import { catalogService } from '@/lib/api/catalog'

try {
  const service = await catalogService.create({
    name: 'Consulta General',
    category: 'Salud',
    description: 'Consulta médica general',
    prices: {
      student: 25.00,
      general: 50.00
    }
  })
  console.log('Servicio creado:', service)
} catch (error) {
  console.error('Error al crear servicio:', error)
}
```

## Perfil de Usuario

### Obtener Mi Perfil
```typescript
import { profileService } from '@/lib/api/profile'

try {
  const profile = await profileService.getMyProfile()
  console.log('Mi perfil:', profile)
} catch (error) {
  console.error('Error al obtener perfil:', error)
}
```

### Actualizar Perfil
```typescript
import { profileService } from '@/lib/api/profile'

try {
  const updated = await profileService.update({
    full_name: 'Juan Pérez Actualizado',
    faculty: 'Ingeniería',
    career: 'Software',
    phone: '+593 999999999'
  })
  console.log('Perfil actualizado:', updated)
} catch (error) {
  console.error('Error al actualizar perfil:', error)
}
```

## Administración

### Obtener Estadísticas del Dashboard
```typescript
import { adminService } from '@/lib/api/admin'

try {
  const stats = await adminService.getDashboardStats()
  console.log('Estadísticas:', stats)
} catch (error) {
  console.error('Error al obtener estadísticas:', error)
}
```

### Estado del Sistema
```typescript
import { adminService } from '@/lib/api/admin'

try {
  const health = await adminService.getSystemHealth()
  console.log('Estado del sistema:', health)
} catch (error) {
  console.error('Error al obtener estado:', error)
}
```

## Uso del Contexto de Autenticación

```typescript
'use client'

import { useAuth } from '@/contexts/AuthContext'

export default function MyComponent() {
  const { user, isAuthenticated, isAdmin, login, logout } = useAuth()

  if (!isAuthenticated) {
    return <div>No autenticado</div>
  }

  return (
    <div>
      <p>Usuario: {user?.email}</p>
      <p>Rol: {user?.role}</p>
      {isAdmin && <p>Eres administrador</p>}
      <button onClick={logout}>Cerrar Sesión</button>
    </div>
  )
}
```

## Manejo de Errores

Todos los servicios API lanzan errores que pueden ser capturados:

```typescript
import { appointmentService } from '@/lib/api/appointments'

try {
  const appointments = await appointmentService.getMyAppointments()
} catch (error: any) {
  if (error.response) {
    // Error de respuesta del servidor
    console.error('Error del servidor:', error.response.data)
    console.error('Status:', error.response.status)
  } else if (error.request) {
    // Error de red
    console.error('Error de red:', error.request)
  } else {
    // Otro error
    console.error('Error:', error.message)
  }
}
```

## Interceptores de Axios

El cliente Axios está configurado para:
- Agregar automáticamente el token JWT a todas las peticiones
- Redirigir a `/login` cuando el token expira (401)
- Manejar errores de red

No necesitas configurar nada adicional, solo usa los servicios API.
