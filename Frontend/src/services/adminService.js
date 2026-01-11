import api from './api';

const adminService = {
  getDashboardStats: async () => {
    try {
      const response = await api.get('/api/admin/dashboard/stats');
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Error al obtener estadísticas' };
    }
  },

  getSystemHealth: async () => {
    try {
      const response = await api.get('/api/admin/monitoring/health');
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Error al obtener estado del sistema' };
    }
  },

  getServiceMetrics: async () => {
    try {
      const response = await api.get('/api/admin/monitoring/metrics');
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Error al obtener métricas' };
    }
  },

  getAllUsers: async (params = {}) => {
    try {
      const response = await api.get('/api/admin/users', { params });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Error al obtener usuarios' };
    }
  },

  updateUserRole: async (userId, role) => {
    try {
      const response = await api.put(`/api/admin/users/${userId}/role`, { role });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Error al actualizar rol' };
    }
  },

  toggleUserStatus: async (userId) => {
    try {
      const response = await api.put(`/api/admin/users/${userId}/toggle-status`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Error al cambiar estado del usuario' };
    }
  },

  generateReport: async (reportType, params = {}) => {
    try {
      const response = await api.get(`/api/admin/reports/${reportType}`, { 
        params,
        responseType: 'blob'
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Error al generar reporte' };
    }
  },

  getSystemLogs: async (params = {}) => {
    try {
      const response = await api.get('/api/admin/logs', { params });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Error al obtener logs' };
    }
  },
};

export default adminService;