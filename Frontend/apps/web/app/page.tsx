'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/contexts/AuthContext'
import Layout from '@/components/layout/Layout'
import { Calendar, Clock, Shield, Users } from 'lucide-react'
import Link from 'next/link'
import Button from '@/components/common/Button'

export default function Home() {
  const router = useRouter()
  const { isAuthenticated, user, isAdmin } = useAuth()

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login')
    }
  }, [isAuthenticated, router])

  if (!isAuthenticated) {
    return null
  }

  return (
    <Layout>
      <div className="space-y-8">
        {/* Hero Section */}
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Bienvenido, {user?.full_name || user?.email}
          </h1>
          <p className="text-xl text-gray-600">
            Sistema de gestión de citas y servicios
          </p>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Link href="/appointments" className="card hover:shadow-lg transition-shadow">
            <Calendar className="h-12 w-12 text-primary-600 mb-4" />
            <h3 className="text-lg font-semibold mb-2">Mis Citas</h3>
            <p className="text-gray-600 text-sm">
              Ver y gestionar tus citas programadas
            </p>
          </Link>

          <Link href="/catalog" className="card hover:shadow-lg transition-shadow">
            <Clock className="h-12 w-12 text-primary-600 mb-4" />
            <h3 className="text-lg font-semibold mb-2">Servicios</h3>
            <p className="text-gray-600 text-sm">
              Explorar servicios disponibles
            </p>
          </Link>

          <Link href="/profile" className="card hover:shadow-lg transition-shadow">
            <Users className="h-12 w-12 text-primary-600 mb-4" />
            <h3 className="text-lg font-semibold mb-2">Mi Perfil</h3>
            <p className="text-gray-600 text-sm">
              Actualizar información personal
            </p>
          </Link>

          {isAdmin && (
            <Link href="/admin" className="card hover:shadow-lg transition-shadow">
              <Shield className="h-12 w-12 text-primary-600 mb-4" />
              <h3 className="text-lg font-semibold mb-2">Administración</h3>
              <p className="text-gray-600 text-sm">
                Panel de control del sistema
              </p>
            </Link>
          )}
        </div>

        {/* User Info */}
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Información de Cuenta</h2>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-gray-600">Email:</span>
              <span className="font-medium">{user?.email}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Tipo de Usuario:</span>
              <span className="font-medium">
                {user?.user_type === 'STUDENT' ? 'Estudiante' : 'General'}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Rol:</span>
              <span className="font-medium">
                {user?.role === 'ADMIN' ? 'Administrador' : 'Usuario'}
              </span>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  )
}
