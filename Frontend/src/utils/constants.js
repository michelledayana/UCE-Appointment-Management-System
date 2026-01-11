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
  // Auth (8081, 8082)
  REGISTER: '/api/auth/register',
  LOGIN: '/api/auth/login',
  LOGOUT: '/api/auth/logout',
  
  // Users (8083)
  PROFILE: '/api/users/profile',
  CHANGE_PASSWORD: '/api/users/password',
  
  // Services (8084)
  SERVICES: '/api/services',
  SERVICE_CATEGORIES: '/api/services/categories',
  SEARCH_SERVICES: '/api/services/search',
  
  // 🆕 Scheduling (8085, 8086)
  SCHEDULES: '/api/schedules',
  SCHEDULE_BY_SERVICE: '/api/schedules/service',
  AVAILABILITY: '/api/appointments/availability', // 8086
  AVAILABILITY_CHECK: '/api/schedules/availability', // 8086
  
  // Appointments (8087, 8088, 8089)
  APPOINTMENTS: '/api/appointments',
  MY_APPOINTMENTS: '/api/appointments/my',
  APPOINTMENT_DETAIL: '/api/appointments', // + /:id
  
  // Admin (8090)
  ADMIN_DASHBOARD: '/api/admin/dashboard/stats',
  ADMIN_USERS: '/api/admin/users',
  ADMIN_MONITORING: '/api/admin/monitoring/health',
  ADMIN_METRICS: '/api/admin/monitoring/metrics',
};