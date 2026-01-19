import apiClient from '@/lib/axios'
import { Profile, UpdateProfileData } from '@/types/profile'

export const profileService = {
  // Obtener mi perfil
  async getMyProfile(): Promise<Profile> {
    const response = await apiClient.get('/profiles/me')
    return response.data
  },

  // Obtener perfil por email
  async getByEmail(email: string): Promise<Profile> {
    const response = await apiClient.get(`/profiles/${email}`)
    return response.data
  },

  // Actualizar perfil
  async update(data: UpdateProfileData): Promise<Profile> {
    const response = await apiClient.put('/profiles/me', data)
    return response.data
  },
}
