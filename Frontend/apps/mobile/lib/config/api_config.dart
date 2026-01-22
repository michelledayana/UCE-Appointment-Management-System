class ApiConfig {
  static const String baseUrl = 'http://10.0.1.245:8000';
  
  // Endpoints
  static const String loginEndpoint = '/auth/login';
  static const String registerEndpoint = '/users/register';
  static const String servicesEndpoint = '/catalog/services';
  static const String appointmentsEndpoint = '/appointments';
  static const String myAppointmentsEndpoint = '/appointments/my';
  
  // Headers
  static Map<String, String> getHeaders(String? token) {
    final headers = <String, String>{
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    };
    
    if (token != null && token.isNotEmpty) {
      headers['Authorization'] = 'Bearer $token';
    }
    
    return headers;
  }
}
