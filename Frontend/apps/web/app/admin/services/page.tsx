'use client'

import { useEffect, useState } from 'react'
import Layout from '@/components/layout/Layout'
import { catalogService } from '@/lib/api/catalog'
import { Service } from '@/types/service'
import ServiceCard from '@/components/services/ServiceCard'
import Loading from '@/components/common/Loading'
import Alert from '@/components/common/Alert'
import Button from '@/components/common/Button'
import { Plus, Edit, Trash2 } from 'lucide-react'
import Link from 'next/link'

export default function AdminServicesPage() {
  const [services, setServices] = useState<Service[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    loadServices()
  }, [])

  const loadServices = async () => {
    try {
      setLoading(true)
      const data = await catalogService.list()
      setServices(Array.isArray(data) ? data : data.services || [])
    } catch (err: any) {
      setError('Error al cargar servicios.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id: string) => {
    if (!confirm('¿Estás seguro de eliminar este servicio?')) {
      return
    }

    try {
      await catalogService.delete(id)
      await loadServices()
    } catch (err: any) {
      alert('Error al eliminar el servicio.')
      console.error(err)
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
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
              Gestión de Servicios
            </h1>
            <p className="mt-2 text-gray-600">
              Administra los servicios disponibles
            </p>
          </div>
          <Link href="/admin/services/new">
            <Button variant="primary">
              <Plus className="h-4 w-4 mr-2" />
              Nuevo Servicio
            </Button>
          </Link>
        </div>

        {error && (
          <Alert type="error" message={error} onClose={() => setError(null)} />
        )}

        {services.length === 0 ? (
          <div className="card text-center py-12">
            <p className="text-gray-600 mb-4">No hay servicios registrados.</p>
            <Link href="/admin/services/new">
              <Button variant="primary">Crear Primer Servicio</Button>
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {services.map((service) => (
              <div key={service.id} className="card">
                <div className="mb-4">
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">
                    {service.name}
                  </h3>
                  <span className="inline-block px-2 py-1 text-xs font-semibold rounded-full bg-primary-100 text-primary-800">
                    {service.category}
                  </span>
                </div>
                <p className="text-gray-600 mb-4">{service.description}</p>
                <div className="flex space-x-2">
                  <Link
                    href={`/admin/services/${service.id}/edit`}
                    className="flex-1"
                  >
                    <Button variant="secondary" className="w-full">
                      <Edit className="h-4 w-4 mr-2" />
                      Editar
                    </Button>
                  </Link>
                  <Button
                    variant="danger"
                    onClick={() => handleDelete(service.id)}
                    className="flex-1"
                  >
                    <Trash2 className="h-4 w-4 mr-2" />
                    Eliminar
                  </Button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </Layout>
  )
}
