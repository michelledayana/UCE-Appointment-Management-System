export interface Service {
  id: string
  name: string
  category: string
  description: string
  is_active: boolean
  prices?: {
    student?: number
    general?: number
  }
}

export interface CreateServiceData {
  name: string
  category: string
  description: string
  prices: {
    student: number
    general: number
  }
}

export interface UpdateServiceData {
  name?: string
  category?: string
  description?: string
  prices?: {
    student?: number
    general?: number
  }
  is_active?: boolean
}
