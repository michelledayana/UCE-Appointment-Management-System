import { Service } from '../../types/service'
import { DollarSign, Calendar } from 'lucide-react'
import Button from '../common/Button'
import Link from 'next/link'

interface ServiceCardProps {
  service: Service
  onBook?: (service: Service) => void
}

export default function ServiceCard({ service, onBook }: ServiceCardProps) {
  return (
    <div className="card hover:shadow-lg transition-shadow">
      <div className="mb-4">
        <h3 className="text-xl font-semibold text-gray-900 mb-2">
          {service.name}
        </h3>
        <span className="inline-block px-2 py-1 text-xs font-semibold rounded-full bg-primary-100 text-primary-800">
          {service.category}
        </span>
      </div>

      <p className="text-gray-600 mb-4">{service.description}</p>

      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-4">
          {service.prices?.student && (
            <div className="flex items-center text-sm text-gray-600">
              <DollarSign className="h-4 w-4 mr-1" />
              Estudiante: ${service.prices.student}
            </div>
          )}
          {service.prices?.general && (
            <div className="flex items-center text-sm text-gray-600">
              <DollarSign className="h-4 w-4 mr-1" />
              General: ${service.prices.general}
            </div>
          )}
        </div>
      </div>

      {service.is_active ? (
        <Button
          variant="primary"
          className="w-full"
          onClick={() => onBook && onBook(service)}
        >
          <Calendar className="h-4 w-4 mr-2" />
          Agendar Cita
        </Button>
      ) : (
        <div className="text-center text-sm text-gray-500 py-2">
          Servicio no disponible
        </div>
      )}
    </div>
  )
}
