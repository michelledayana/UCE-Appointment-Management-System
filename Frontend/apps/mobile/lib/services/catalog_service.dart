import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config/api_config.dart';
import '../models/service_model.dart';
import 'storage_service.dart';

class CatalogService {
  static Future<List<Service>> getServices() async {
    try {
      final token = await StorageService.getToken();
      final response = await http.get(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.servicesEndpoint}'),
        headers: ApiConfig.getHeaders(token),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        if (data is List) {
          return data.map((json) => Service.fromJson(json)).toList();
        }
        return [];
      } else {
        throw Exception('Error al obtener servicios');
      }
    } catch (e) {
      throw Exception('Error de conexión: ${e.toString()}');
    }
  }

  static Future<Service> getServiceById(String id) async {
    try {
      final token = await StorageService.getToken();
      final response = await http.get(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.servicesEndpoint}/$id'),
        headers: ApiConfig.getHeaders(token),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return Service.fromJson(data);
      } else {
        throw Exception('Error al obtener el servicio');
      }
    } catch (e) {
      throw Exception('Error de conexión: ${e.toString()}');
    }
  }
}
