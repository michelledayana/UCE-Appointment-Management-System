export interface Profile {
  email: string
  full_name: string
  user_type: 'STUDENT' | 'GENERAL'
  faculty?: string
  career?: string
  phone?: string
}

export interface UpdateProfileData {
  full_name?: string
  faculty?: string
  career?: string
  phone?: string
}
