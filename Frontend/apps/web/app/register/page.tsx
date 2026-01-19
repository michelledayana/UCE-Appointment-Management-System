'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/contexts/AuthContext'
import { useForm } from 'react-hook-form'
import Link from 'next/link'
import Input from '@/components/common/Input'
import Button from '@/components/common/Button'
import Alert from '@/components/common/Alert'
import { Calendar } from 'lucide-react'

interface RegisterForm {
  full_name: string
  email: string
  password: string
}

export default function RegisterPage() {
  const router = useRouter()
  const { register: registerUser, login, isAuthenticated } = useAuth()
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterForm>()

  // Si ya está autenticado, redirigir
  if (isAuthenticated) {
    router.push('/')
    return null
  }

  const onSubmit = async (data: RegisterForm) => {
    setError(null)
    setLoading(true)

    try {
      // Primero registrar el usuario
      await registerUser({
        full_name: data.full_name,
        email: data.email,
        password: data.password,
      })
      
      // Después del registro, hacer login automático para obtener el token
      await login({
        email: data.email,
        password: data.password,
      })
      
      router.push('/')
    } catch (err: any) {
      console.error('Error completo:', err)
      
      let errorMessage = 'Error al registrar. Intenta nuevamente.'
      
      if (err.response) {
        // Error de respuesta del servidor
        const data = err.response.data
        errorMessage = data?.detail || data?.message || `Error ${err.response.status}: ${err.response.statusText}`
      } else if (err.request) {
        // Error de red (no hay respuesta del servidor)
        errorMessage = 'No se pudo conectar con el servidor. Verifica que el API Gateway esté corriendo.'
      } else {
        // Otro tipo de error
        errorMessage = err.message || errorMessage
      }
      
      setError(errorMessage)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <div className="flex justify-center">
            <Calendar className="h-12 w-12 text-primary-600" />
          </div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Crear Cuenta
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            O{' '}
            <Link
              href="/login"
              className="font-medium text-primary-600 hover:text-primary-500"
            >
              inicia sesión con tu cuenta
            </Link>
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit(onSubmit)}>
          {error && (
            <Alert type="error" message={error} onClose={() => setError(null)} />
          )}

          <div className="space-y-4">
            <Input
              label="Nombre Completo"
              type="text"
              autoComplete="name"
              {...register('full_name', {
                required: 'El nombre es requerido',
                minLength: {
                  value: 3,
                  message: 'El nombre debe tener al menos 3 caracteres',
                },
              })}
              error={errors.full_name?.message}
            />

            <Input
              label="Email"
              type="email"
              autoComplete="email"
              {...register('email', {
                required: 'El email es requerido',
                pattern: {
                  value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                  message: 'Email inválido',
                },
              })}
              error={errors.email?.message}
            />

            <Input
              label="Contraseña"
              type="password"
              autoComplete="new-password"
              {...register('password', {
                required: 'La contraseña es requerida',
                minLength: {
                  value: 6,
                  message: 'La contraseña debe tener al menos 6 caracteres',
                },
              })}
              error={errors.password?.message}
            />
          </div>

          <Button type="submit" variant="primary" className="w-full" loading={loading}>
            Registrarse
          </Button>
        </form>
      </div>
    </div>
  )
}
