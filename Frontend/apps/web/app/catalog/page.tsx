'use client'

import { useEffect, useState } from 'react'
import Layout from '@/components/layout/Layout'
import { catalogService } from '@/lib/api/catalog'
import { Service } from '@/types/service'
import ServiceCard from '@/components/services/ServiceCard'
import Loading from '@/components/common/Loading'
import Alert from '@/components/common/Alert'
import { useRouter } from 'next/navigation'

export default function CatalogPage() {
  const router = useRouter()
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
      setError('Error al cargar servicios. Intenta nuevamente.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleBookService = (service: Service) => {
    router.push(`/appointments/new?serviceId=${service.id}&serviceName=${encodeURIComponent(service.name)}`)
  }

  if (loading) {
    return (
      <Layout>
        <Loading />
      </Layout>
    )
  }

  return (
    <Layout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Catálogo de Servicios</h1>
          <p className="mt-2 text-gray-600">
            Explora nuestros servicios disponibles y agenda tu cita
          </p>
        </div>

        {error && (
          <Alert type="error" message={error} onClose={() => setError(null)} />
        )}

        {services.length === 0 ? (
          <div className="card text-center py-12">
            <p className="text-gray-600">No hay servicios disponibles en este momento.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {services.map((service) => (
              <ServiceCard
                key={service.id}
                service={service}
                onBook={handleBookService}
              />
            ))}
          </div>
        )}
      </div>
    </Layout>
  )
}
