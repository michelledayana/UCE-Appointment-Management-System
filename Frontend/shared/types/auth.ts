export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterData {
  full_name: string
  email: string
  password: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
  user?: {
    id: string
    email: string
    full_name: string
    role: 'ADMIN' | 'USUARIO'
    user_type?: 'STUDENT' | 'GENERAL'
  }
}

export interface User {
  id: string
  email: string
  full_name: string
  role: 'ADMIN' | 'USUARIO'
  user_type?: 'STUDENT' | 'GENERAL'
}
