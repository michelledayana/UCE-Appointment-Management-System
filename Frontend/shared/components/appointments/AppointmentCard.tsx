import { Appointment } from '@/types/appointment'
import { format } from 'date-fns'
import { Calendar, Clock, DollarSign, X } from 'lucide-react'
import Button from '@/components/common/Button'

interface AppointmentCardProps {
  appointment: Appointment
  onCancel?: (id: string) => void
  showActions?: boolean
}

export default function AppointmentCard({
  appointment,
  onCancel,
  showActions = true,
}: AppointmentCardProps) {
  const statusColors = {
    SCHEDULED: 'bg-blue-100 text-blue-800',
    COMPLETED: 'bg-green-100 text-green-800',
    CANCELLED: 'bg-red-100 text-red-800',
  }

  const statusLabels = {
    SCHEDULED: 'Programada',
    COMPLETED: 'Completada',
    CANCELLED: 'Cancelada',
  }

  return (
    <div className="card hover:shadow-lg transition-shadow">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">
            {appointment.service_name}
          </h3>
          <span
            className={`inline-block px-2 py-1 text-xs font-semibold rounded-full ${
              statusColors[appointment.status]
            }`}
          >
            {statusLabels[appointment.status]}
          </span>
        </div>
        {showActions && appointment.status === 'SCHEDULED' && onCancel && (
          <Button
            variant="danger"
            onClick={() => onCancel(appointment.id)}
            className="text-sm"
          >
            <X className="h-4 w-4" />
          </Button>
        )}
      </div>

      <div className="space-y-2 text-sm text-gray-600">
        <div className="flex items-center">
          <Calendar className="h-4 w-4 mr-2" />
          {format(new Date(appointment.appointment_date), 'PPP')}
        </div>
        <div className="flex items-center">
          <Clock className="h-4 w-4 mr-2" />
          {format(new Date(appointment.appointment_date), 'HH:mm')}
        </div>
        <div className="flex items-center">
          <DollarSign className="h-4 w-4 mr-2" />
          ${appointment.price.toFixed(2)}
        </div>
      </div>
    </div>
  )
}
