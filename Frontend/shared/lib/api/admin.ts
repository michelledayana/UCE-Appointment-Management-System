import apiClient from '@/lib/axios'

export const adminService = {
  // Health check
  async health(): Promise<any> {
    const response = await apiClient.get('/admin/health')
    return response.data
  },

  // Estadísticas del dashboard
  async getDashboardStats(): Promise<any> {
    const response = await apiClient.get('/admin/dashboard/stats')
    return response.data
  },

  // Estado del sistema
  async getSystemHealth(): Promise<any> {
    const response = await apiClient.get('/admin/monitoring/health')
    return response.data
  },

  // Métricas del sistema
  async getMetrics(): Promise<any> {
    const response = await apiClient.get('/admin/monitoring/metrics')
    return response.data
  },
}
