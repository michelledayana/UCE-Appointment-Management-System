'use client'

import { useEffect, useState } from 'react'
import Layout from '@/components/layout/Layout'
import { appointmentService } from '@/lib/api/appointments'
import { Appointment } from '@/types/appointment'
import AppointmentCard from '@/components/appointments/AppointmentCard'
import Loading from '@/components/common/Loading'
import Alert from '@/components/common/Alert'
import Button from '@/components/common/Button'
import { Plus } from 'lucide-react'
import Link from 'next/link'

export default function AppointmentsPage() {
  const [appointments, setAppointments] = useState<Appointment[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    loadAppointments()
  }, [])

  const loadAppointments = async () => {
    try {
      setLoading(true)
      const data = await appointmentService.getMyAppointments()
      setAppointments(Array.isArray(data) ? data : [])
    } catch (err: any) {
      setError('Error al cargar citas. Intenta nuevamente.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleCancel = async (id: string) => {
    if (!confirm('¿Estás seguro de cancelar esta cita?')) {
      return
    }

    try {
      await appointmentService.cancel(id)
      await loadAppointments()
    } catch (err: any) {
      alert('Error al cancelar la cita. Intenta nuevamente.')
      console.error(err)
    }
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
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Mis Citas</h1>
            <p className="mt-2 text-gray-600">
              Gestiona tus citas programadas
            </p>
          </div>
          <Link href="/appointments/new">
            <Button variant="primary">
              <Plus className="h-4 w-4 mr-2" />
              Nueva Cita
            </Button>
          </Link>
        </div>

        {error && (
          <Alert type="error" message={error} onClose={() => setError(null)} />
        )}

        {appointments.length === 0 ? (
          <div className="card text-center py-12">
            <p className="text-gray-600 mb-4">No tienes citas programadas.</p>
            <Link href="/appointments/new">
              <Button variant="primary">Agendar Primera Cita</Button>
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {appointments.map((appointment) => (
              <AppointmentCard
                key={appointment.id}
                appointment={appointment}
                onCancel={handleCancel}
              />
            ))}
          </div>
        )}
      </div>
    </Layout>
  )
}
