import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config/api_config.dart';
import '../models/appointment_model.dart';
import 'storage_service.dart';

class AppointmentService {
  static Future<Appointment> createAppointment(CreateAppointmentData data) async {
    try {
      final token = await StorageService.getToken();
      final response = await http.post(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.appointmentsEndpoint}'),
        headers: ApiConfig.getHeaders(token),
        body: jsonEncode(data.toJson()),
      );

      if (response.statusCode == 200 || response.statusCode == 201) {
        final responseData = jsonDecode(response.body);
        return Appointment.fromJson(responseData);
      } else {
        final error = jsonDecode(response.body);
        throw Exception(error['detail'] ?? 'Error al crear la cita');
      }
    } catch (e) {
      if (e is Exception) {
        rethrow;
      }
      throw Exception('Error de conexión: ${e.toString()}');
    }
  }

  static Future<List<Appointment>> getMyAppointments() async {
    try {
      final token = await StorageService.getToken();
      final response = await http.get(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.myAppointmentsEndpoint}'),
        headers: ApiConfig.getHeaders(token),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        if (data is List) {
          return data.map((json) => Appointment.fromJson(json)).toList();
        }
        return [];
      } else {
        throw Exception('Error al obtener citas');
      }
    } catch (e) {
      throw Exception('Error de conexión: ${e.toString()}');
    }
  }
}
