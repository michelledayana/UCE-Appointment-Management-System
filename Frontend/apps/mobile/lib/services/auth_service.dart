import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config/api_config.dart';
import '../models/auth_model.dart';
import 'storage_service.dart';

class AuthService {
  static Future<AuthResponse> login(LoginCredentials credentials) async {
    try {
      final response = await http.post(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.loginEndpoint}'),
        headers: ApiConfig.getHeaders(null),
        body: jsonEncode(credentials.toJson()),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final authResponse = AuthResponse.fromJson(data);
        
        // Guardar token
        await StorageService.saveToken(authResponse.accessToken);
        if (authResponse.user != null) {
          await StorageService.saveUserEmail(authResponse.user!.email);
        }
        
        return authResponse;
      } else {
        final error = jsonDecode(response.body);
        throw Exception(error['detail'] ?? 'Error al iniciar sesión');
      }
    } catch (e) {
      if (e is Exception) {
        rethrow;
      }
      throw Exception('Error de conexión: ${e.toString()}');
    }
  }

  static Future<Map<String, dynamic>> register(RegisterData data) async {
    try {
      final response = await http.post(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.registerEndpoint}'),
        headers: ApiConfig.getHeaders(null),
        body: jsonEncode(data.toJson()),
      );

      if (response.statusCode == 200 || response.statusCode == 201) {
        return jsonDecode(response.body);
      } else {
        final error = jsonDecode(response.body);
        throw Exception(error['detail'] ?? 'Error al registrar usuario');
      }
    } catch (e) {
      if (e is Exception) {
        rethrow;
      }
      throw Exception('Error de conexión: ${e.toString()}');
    }
  }

  static Future<void> logout() async {
    await StorageService.clearAll();
  }

  static Future<String?> getStoredToken() async {
    return await StorageService.getToken();
  }
}
