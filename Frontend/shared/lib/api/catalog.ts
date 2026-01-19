import apiClient from '@/lib/axios'
import { Service, CreateServiceData, UpdateServiceData } from '@/types/service'

export const catalogService = {
  // Listar servicios
  async list(): Promise<Service[]> {
    const response = await apiClient.get('/catalog/services')
    return response.data
  },

  // Obtener servicio por ID
  async getById(id: string): Promise<Service> {
    const response = await apiClient.get(`/catalog/services/${id}`)
    return response.data
  },

  // Crear servicio (Admin)
  async create(data: CreateServiceData): Promise<Service> {
    const response = await apiClient.post('/catalog/services', data)
    return response.data
  },

  // Actualizar servicio (Admin)
  async update(id: string, data: UpdateServiceData): Promise<Service> {
    const response = await apiClient.put(`/catalog/services/${id}`, data)
    return response.data
  },

  // Eliminar servicio (Admin)
  async delete(id: string): Promise<void> {
    await apiClient.delete(`/catalog/services/${id}`)
  },
}
