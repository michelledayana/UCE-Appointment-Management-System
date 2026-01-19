import api from './api';

const appointmentService = {
  getMyAppointments: async () => {
    try {
      const response = await api.get('/appointments/my');
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Error al obtener citas' };
    }
  },

  getAllAppointments: async (params = {}) => {
    try {
      const response = await api.get('/appointments', { params });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Error al obtener citas' };
    }
  },

  getAppointmentById: async (id) => {
    try {
      const response = await api.get(`/appointments/${id}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Error al obtener la cita' };
    }
  },

  createAppointment: async (appointmentData) => {
    try {
      const response = await api.post('/appointments', appointmentData);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Error al crear la cita' };
    }
  },

  updateAppointment: async (id, appointmentData) => {
    try {
      const response = await api.patch(`/appointments/${id}`, appointmentData);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Error al actualizar la cita' };
    }
  },

  cancelAppointment: async (id) => {
    try {
      const response = await api.delete(`/appointments/${id}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Error al cancelar la cita' };
    }
  },

  checkAvailability: async (serviceId, date) => {
    try {
      const response = await api.get('/appointments/availability', {
        params: { serviceId, date }
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Error al verificar disponibilidad' };
    }
  },
};

export default appointmentService;