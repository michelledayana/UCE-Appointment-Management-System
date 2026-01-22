import apiClient from '../axios'
import { LoginCredentials, RegisterData, AuthResponse } from '../../types/auth'

export const authService = {
  // Login
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const response = await apiClient.post('/auth/login', credentials)
    return response.data
  },

  // Registro
  async register(data: RegisterData): Promise<any> {
    const response = await apiClient.post('/users/register', data)
    return response.data
  },

  // Logout (solo limpia cookies, no necesita llamada al servidor)
  logout() {
    // Se maneja en el contexto de autenticación
  },
}
