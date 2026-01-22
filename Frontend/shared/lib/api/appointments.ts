import apiClient from '../axios'
import { Appointment, CreateAppointmentData, UpdateAppointmentData } from '../../types/appointment'

export const appointmentService = {
  // Crear cita
  async create(data: CreateAppointmentData): Promise<Appointment> {
    const response = await apiClient.post('/appointments', data)
    return response.data
  },

  // Listar todas las citas (Admin)
  async listAll(): Promise<Appointment[]> {
    const response = await apiClient.get('/appointments')
    return response.data
  },

  // Obtener mis citas
  async getMyAppointments(): Promise<Appointment[]> {
    const response = await apiClient.get('/appointments/my')
    return response.data
  },

  // Obtener cita por ID
  async getById(id: string): Promise<Appointment> {
    const response = await apiClient.get(`/appointments/${id}`)
    return response.data
  },

  // Actualizar cita
  async update(id: string, data: UpdateAppointmentData): Promise<Appointment> {
    const response = await apiClient.patch(`/appointments/${id}`, data)
    return response.data
  },

  // Cancelar cita
  async cancel(id: string): Promise<Appointment> {
    const response = await apiClient.patch(`/appointments/${id}`, { status: 'cancelled' })
    return response.data
  },

  // Verificar disponibilidad
  async checkAvailability(serviceId?: string, date?: string) {
    const response = await apiClient.get('/appointments/availability', {
      params: { serviceId, date },
    })
    return response.data
  },
}
