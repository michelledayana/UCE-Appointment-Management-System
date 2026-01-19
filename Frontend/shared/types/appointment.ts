export interface Appointment {
  id: string
  user_email: string
  service_name: string
  appointment_date: string
  price: number
  status: 'SCHEDULED' | 'COMPLETED' | 'CANCELLED'
  created_at?: string
  updated_at?: string
}

export interface CreateAppointmentData {
  user_email: string
  service_name: string
  appointment_date: string
}

export interface UpdateAppointmentData {
  service_name?: string
  appointment_date?: string
  status?: 'SCHEDULED' | 'COMPLETED' | 'CANCELLED'
}
