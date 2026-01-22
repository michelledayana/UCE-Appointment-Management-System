export const USER_ROLES = {
  ADMIN: 'ADMIN',
  USER: 'USUARIO',
};

export const APPOINTMENT_STATUS = {
  PENDING: 'pending',
  CONFIRMED: 'confirmed',
  CANCELLED: 'cancelled',
  COMPLETED: 'completed',
};

export const SERVICE_CATEGORIES = {
  CONSULTATION: 'consulta',
  THERAPY: 'terapia',
  DIAGNOSTIC: 'diagnostico',
};

export const API_ENDPOINTS = {
  // Auth
  LOGIN: '/auth/login',
  REGISTER: '/users/register',
  LOGOUT: '/auth/logout',
  
  // Users & Profile
  PROFILE: '/profiles/me',
  PROFILE_BY_EMAIL: '/profiles',
  CHANGE_PASSWORD: '/users/password',
  
  // Services
  SERVICES: '/catalog/services',
  SERVICE_DETAIL: '/catalog/services',
  
  // Schedules
  SCHEDULES: '/scheduling',
  AVAILABILITY: '/appointments/availability',
  
  // Appointments
  APPOINTMENTS: '/appointments',
  MY_APPOINTMENTS: '/appointments/my',
  
  // Admin
  ADMIN_HEALTH: '/admin/health',
  ADMIN_DASHBOARD: '/admin/dashboard/stats',
  ADMIN_MONITORING: '/admin/monitoring/health',
  ADMIN_METRICS: '/admin/monitoring/metrics',
};