'use client'

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import Cookies from 'js-cookie'
import { authService } from '../lib/api/auth'
import { User, LoginCredentials, RegisterData } from '../types/auth'

interface AuthContextType {
  user: User | null
  loading: boolean
  login: (credentials: LoginCredentials) => Promise<void>
  register: (data: RegisterData) => Promise<void>
  logout: () => void
  isAuthenticated: boolean
  isAdmin: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  // Cargar usuario desde cookies al iniciar
  useEffect(() => {
    const loadUser = () => {
      try {
        const userCookie = Cookies.get('user')
        if (userCookie) {
          setUser(JSON.parse(userCookie))
        }
      } catch (error) {
        console.error('Error loading user from cookies:', error)
        Cookies.remove('user')
        Cookies.remove('token')
      } finally {
        setLoading(false)
      }
    }

    loadUser()
  }, [])

  const login = async (credentials: LoginCredentials) => {
    try {
      const response = await authService.login(credentials)
      
      // Guardar token y usuario en cookies
      Cookies.set('token', response.access_token, { expires: 7 }) // 7 días
      
      if (response.user) {
        Cookies.set('user', JSON.stringify(response.user), { expires: 7 })
        setUser(response.user)
      } else {
        // Si no viene el usuario en la respuesta, extraer del token
        // Por ahora, crear un usuario básico
        const basicUser: User = {
          id: '',
          email: credentials.email,
          full_name: '',
          role: 'USUARIO',
        }
        Cookies.set('user', JSON.stringify(basicUser), { expires: 7 })
        setUser(basicUser)
      }
    } catch (error: any) {
      console.error('Login error:', error)
      throw error
    }
  }

  const register = async (data: RegisterData) => {
    try {
      const response = await authService.register(data)
      
      // El servicio de registro devuelve:
      // {
      //   "status": "success",
      //   "message": "User registered successfully",
      //   "data": { id, email, full_name, user_type }
      // }
      
      // No devuelve token, solo los datos del usuario
      // El token se obtiene haciendo login después del registro
      
      if (response.data) {
        // Guardar usuario temporalmente (sin token aún)
        const userData: User = {
          id: response.data.id?.toString() || '',
          email: response.data.email,
          full_name: response.data.full_name,
          role: 'USUARIO', // Por defecto es USUARIO, no ADMIN
          user_type: response.data.user_type,
        }
        // No guardamos en cookies aún, se hará después del login
        return response
      }
      
      return response
    } catch (error: any) {
      console.error('Register error:', error)
      throw error
    }
  }

  const logout = () => {
    Cookies.remove('token')
    Cookies.remove('user')
    setUser(null)
    if (typeof window !== 'undefined') {
      window.location.href = '/login'
    }
  }

  const value: AuthContextType = {
    user,
    loading,
    login,
    register,
    logout,
    isAuthenticated: !!user,
    isAdmin: user?.role === 'ADMIN',
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
