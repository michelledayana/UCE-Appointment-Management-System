import api from './api';

const authService = {
  login: async (credentials) => {
    try {
      const response = await api.post('/auth/login', credentials);
      
      console.log('Login response COMPLETO:', JSON.stringify(response.data, null, 2));
      
      const data = response.data;
      const token = data.token || data.access_token || data.accessToken;
      const user = data.user || data.data || data;
      
      console.log('Token extraído:', token);
      console.log('User extraído:', JSON.stringify(user, null, 2));
      
      if (typeof window !== 'undefined') {
        if (token) {
          localStorage.setItem('token', token);
        }
        localStorage.setItem('user', JSON.stringify(user));
      }
      
      return { token, user };
    } catch (error) {
      console.error('Login error:', error.response?.data || error);
      throw error.response?.data || { message: 'Error al iniciar sesión' };
    }
  },

  register: async (userData) => {
    try {
      const response = await api.post('/users/register', userData);
      console.log('Register response:', response.data);
      return response.data;
    } catch (error) {
      console.error('Register error:', error.response?.data || error);
      throw error.response?.data || { message: 'Error al registrar usuario' };
    }
  },

  logout: () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
    }
  },

  getCurrentUser: () => {
    if (typeof window !== 'undefined') {
      const userStr = localStorage.getItem('user');
      try {
        return userStr ? JSON.parse(userStr) : null;
      } catch (e) {
        console.error('Error parsing user:', e);
        return null;
      }
    }
    return null;
  },

  isAuthenticated: () => {
    if (typeof window !== 'undefined') {
      return !!localStorage.getItem('token');
    }
    return false;
  },

  hasRole: (role) => {
    const user = authService.getCurrentUser();
    if (!user) return false;
    
    const userRole = user.role || user.roles?.[0] || 'USUARIO';
    return userRole === role;
  },

  updateProfile: async (userData) => {
    try {
      const response = await api.put('/profiles/me', userData);
      const updatedUser = response.data;
      if (typeof window !== 'undefined') {
        localStorage.setItem('user', JSON.stringify(updatedUser));
      }
      return updatedUser;
    } catch (error) {
      console.error('Update profile error:', error.response?.data || error);
      throw error.response?.data || { message: 'Error al actualizar perfil' };
    }
  },

  changePassword: async (passwordData) => {
    try {
      const response = await api.put('/users/password', passwordData);
      return response.data;
    } catch (error) {
      console.error('Change password error:', error.response?.data || error);
      throw error.response?.data || { message: 'Error al cambiar contraseña' };
    }
  },
};

export default authService;