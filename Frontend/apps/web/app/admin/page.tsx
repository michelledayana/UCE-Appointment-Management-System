'use client'

import { useEffect, useState } from 'react'
import Layout from '@/components/layout/Layout'
import { adminService, catalogService, appointmentService } from '@/lib/api'
import { Service, CreateServiceData } from '@/types/service'
import { useForm } from 'react-hook-form'
import Input from '@/components/common/Input'
import Button from '@/components/common/Button'
import Alert from '@/components/common/Alert'
import Loading from '@/components/common/Loading'
import { Activity, Users, Calendar, DollarSign, Server, TrendingUp } from 'lucide-react'

export default function AdminPage() {
  const [stats, setStats] = useState<any>(null)
  const [systemHealth, setSystemHealth] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadDashboardData()
  }, [])

  const loadDashboardData = async () => {
    try {
      setLoading(true)
      const [statsData, healthData] = await Promise.all([
        adminService.getDashboardStats(),
        adminService.getSystemHealth(),
      ])
      setStats(statsData)
      setSystemHealth(healthData)
    } catch (err) {
      console.error('Error loading dashboard data:', err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <Layout requireAdmin>
        <Loading />
      </Layout>
    )
  }

  return (
    <Layout requireAdmin>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Panel de Administración</h1>
          <p className="mt-2 text-gray-600">
            Gestión y monitoreo del sistema
          </p>
        </div>

        {/* Stats Cards */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="card">
              <div className="flex items-center">
                <Users className="h-8 w-8 text-primary-600" />
                <div className="ml-4">
                  <p className="text-sm text-gray-600">Total Usuarios</p>
                  <p className="text-2xl font-bold">{stats.totalUsers || 0}</p>
                </div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-center">
                <Calendar className="h-8 w-8 text-green-600" />
                <div className="ml-4">
                  <p className="text-sm text-gray-600">Citas Hoy</p>
                  <p className="text-2xl font-bold">
                    {stats.appointmentsToday || 0}
                  </p>
                </div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-center">
                <Activity className="h-8 w-8 text-blue-600" />
                <div className="ml-4">
                  <p className="text-sm text-gray-600">Servicios Activos</p>
                  <p className="text-2xl font-bold">
                    {stats.activeServices || 0}
                  </p>
                </div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-center">
                <DollarSign className="h-8 w-8 text-yellow-600" />
                <div className="ml-4">
                  <p className="text-sm text-gray-600">Ingresos Mensuales</p>
                  <p className="text-2xl font-bold">
                    ${stats.monthlyRevenue || 0}
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* System Health */}
        {systemHealth && (
          <div className="card">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <Server className="h-5 w-5 mr-2" />
              Estado del Sistema
            </h2>
            <div className="space-y-3">
              {systemHealth.services?.map((service: any, index: number) => (
                <div
                  key={index}
                  className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                >
                  <div>
                    <p className="font-medium">{service.name}</p>
                    <p className="text-sm text-gray-600">
                      Uptime: {service.uptime} | Response: {service.responseTime}
                    </p>
                  </div>
                  <span
                    className={`px-3 py-1 rounded-full text-sm font-semibold ${
                      service.status === 'healthy'
                        ? 'bg-green-100 text-green-800'
                        : 'bg-red-100 text-red-800'
                    }`}
                  >
                    {service.status === 'healthy' ? 'Activo' : 'Inactivo'}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="card">
            <h2 className="text-xl font-semibold mb-4">Gestión de Servicios</h2>
            <div className="space-y-2">
              <a href="/admin/services">
                <Button variant="primary" className="w-full">
                  Ver Todos los Servicios
                </Button>
              </a>
              <a href="/admin/services/new">
                <Button variant="secondary" className="w-full">
                  Crear Nuevo Servicio
                </Button>
              </a>
            </div>
          </div>

          <div className="card">
            <h2 className="text-xl font-semibold mb-4">Gestión de Citas</h2>
            <div className="space-y-2">
              <a href="/admin/appointments">
                <Button variant="primary" className="w-full">
                  Ver Todas las Citas
                </Button>
              </a>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  )
}
