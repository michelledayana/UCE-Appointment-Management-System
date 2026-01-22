'use client'

import { useEffect, useState } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import Layout from '@/components/layout/Layout'
import { appointmentService } from '@/lib/api/appointments'
import { catalogService } from '@/lib/api/catalog'
import { Service } from '@/types/service'
import { useForm } from 'react-hook-form'
import Input from '@/components/common/Input'
import Button from '@/components/common/Button'
import Alert from '@/components/common/Alert'
import { useAuth } from '@/contexts/AuthContext'

interface AppointmentForm {
  service_name: string
  appointment_date: string
  appointment_time: string
}

export default function NewAppointmentPage() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const { user } = useAuth()
  const [services, setServices] = useState<Service[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [selectedService, setSelectedService] = useState<Service | null>(null)

  const {
    register,
    handleSubmit,
    formState: { errors },
    setValue,
  } = useForm<AppointmentForm>()

  useEffect(() => {
    loadServices()
    const serviceId = searchParams.get('serviceId')
    const serviceName = searchParams.get('serviceName')
    if (serviceId && serviceName) {
      setValue('service_name', serviceName)
    }
  }, [searchParams, setValue])

  const loadServices = async () => {
    try {
      const data = await catalogService.list()
      const servicesList = Array.isArray(data) ? data : data.services || []
      setServices(servicesList)
      
      const serviceId = searchParams.get('serviceId')
      if (serviceId) {
        const service = servicesList.find((s: Service) => s.id === serviceId)
        if (service) {
          setSelectedService(service)
        }
      }
    } catch (err) {
      console.error('Error loading services:', err)
    }
  }

  const onSubmit = async (data: AppointmentForm) => {
    setError(null)
    setLoading(true)

    try {
      const appointmentDateTime = new Date(`${data.appointment_date}T${data.appointment_time}`)
      
      await appointmentService.create({
        user_email: user?.email || '',
        service_name: data.service_name,
        appointment_date: appointmentDateTime.toISOString(),
      })
      
      router.push('/appointments')
    } catch (err: any) {
      setError(
        err.response?.data?.detail ||
          'Error al crear la cita. Intenta nuevamente.'
      )
    } finally {
      setLoading(false)
    }
  }

  const minDate = new Date().toISOString().split('T')[0]

  return (
    <Layout>
      <div className="max-w-2xl mx-auto">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Nueva Cita</h1>
          <p className="mt-2 text-gray-600">
            Completa el formulario para agendar una nueva cita
          </p>
        </div>

        {error && (
          <Alert type="error" message={error} onClose={() => setError(null)} />
        )}

        <form onSubmit={handleSubmit(onSubmit)} className="card space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Servicio
            </label>
            <select
              {...register('service_name', {
                required: 'Selecciona un servicio',
              })}
              className="input"
              onChange={(e) => {
                const service = services.find((s) => s.name === e.target.value)
                setSelectedService(service || null)
                setValue('service_name', e.target.value)
              }}
            >
              <option value="">Selecciona un servicio</option>
              {services
                .filter((s) => s.is_active)
                .map((service) => (
                  <option key={service.id} value={service.name}>
                    {service.name} - ${service.prices?.general || 'N/A'}
                  </option>
                ))}
            </select>
            {errors.service_name && (
              <p className="mt-1 text-sm text-red-600">
                {errors.service_name.message}
              </p>
            )}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input
              label="Fecha"
              type="date"
              min={minDate}
              {...register('appointment_date', {
                required: 'La fecha es requerida',
              })}
              error={errors.appointment_date?.message}
            />

            <Input
              label="Hora"
              type="time"
              {...register('appointment_time', {
                required: 'La hora es requerida',
              })}
              error={errors.appointment_time?.message}
            />
          </div>

          {selectedService && (
            <div className="bg-primary-50 p-4 rounded-lg">
              <p className="text-sm text-gray-600">
                <strong>Servicio seleccionado:</strong> {selectedService.name}
              </p>
              <p className="text-sm text-gray-600">
                <strong>Precio:</strong> $
                {user?.user_type === 'STUDENT' && selectedService.prices?.student
                  ? selectedService.prices.student
                  : selectedService.prices?.general || 'N/A'}
              </p>
            </div>
          )}

          <div className="flex space-x-4">
            <Button
              type="button"
              variant="secondary"
              onClick={() => router.back()}
              className="flex-1"
            >
              Cancelar
            </Button>
            <Button
              type="submit"
              variant="primary"
              loading={loading}
              className="flex-1"
            >
              Agendar Cita
            </Button>
          </div>
        </form>
      </div>
    </Layout>
  )
}
