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

interface LoginForm {
  email: string
  password: string
}

export default function LoginPage() {
  const router = useRouter()
  const { login, isAuthenticated } = useAuth()
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginForm>()

  // Si ya está autenticado, redirigir
  if (isAuthenticated) {
    router.push('/')
    return null
  }

  const onSubmit = async (data: LoginForm) => {
    setError(null)
    setLoading(true)

    try {
      await login(data)
      router.push('/')
    } catch (err: any) {
      setError(
        err.response?.data?.detail ||
          'Error al iniciar sesión. Verifica tus credenciales.'
      )
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
            Iniciar Sesión
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            O{' '}
            <Link
              href="/register"
              className="font-medium text-primary-600 hover:text-primary-500"
            >
              crea una cuenta nueva
            </Link>
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit(onSubmit)}>
          {error && (
            <Alert type="error" message={error} onClose={() => setError(null)} />
          )}

          <div className="space-y-4">
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
              autoComplete="current-password"
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
            Iniciar Sesión
          </Button>
        </form>
      </div>
    </div>
  )
}
