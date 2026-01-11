import api from './api';

const serviceService = {
  getAllServices: async (params = {}) => {
    try {
      const response = await api.get('/api/services', { params });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Error al obtener servicios' };
    }
  },

  getServiceById: async (id) => {
    try {
      const response = await api.get(`/api/services/${id}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Error al obtener el servicio' };
    }
  },

  createService: async (serviceData) => {
    try {
      const response = await api.post('/api/services', serviceData);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Error al crear el servicio' };
    }
  },

  updateService: async (id, serviceData) => {
    try {
      const response = await api.put(`/api/services/${id}`, serviceData);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Error al actualizar el servicio' };
    }
  },

  deleteService: async (id) => {
    try {
      const response = await api.delete(`/api/services/${id}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Error al eliminar el servicio' };
    }
  },

  searchServices: async (query) => {
    try {
      const response = await api.get('/api/services/search', {
        params: { q: query }
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Error en la búsqueda' };
    }
  },

  getCategories: async () => {
    try {
      const response = await api.get('/api/services/categories');
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Error al obtener categorías' };
    }
  },
};

export default serviceService;