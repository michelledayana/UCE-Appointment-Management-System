import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../services/appointment_service.dart';
import '../models/appointment_model.dart';
import '../models/service_model.dart';
import '../services/storage_service.dart';
import 'home_screen.dart';

class CreateAppointmentScreen extends StatefulWidget {
  final Service service;

  const CreateAppointmentScreen({
    super.key,
    required this.service,
  });

  @override
  State<CreateAppointmentScreen> createState() =>
      _CreateAppointmentScreenState();
}

class _CreateAppointmentScreenState extends State<CreateAppointmentScreen> {
  DateTime? _selectedDate;
  TimeOfDay? _selectedTime;
  bool _isLoading = false;
  String? _errorMessage;

  Future<void> _selectDate() async {
    final DateTime now = DateTime.now();
    final DateTime firstDate = now;
    final DateTime lastDate = now.add(const Duration(days: 30));

    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: now,
      firstDate: firstDate,
      lastDate: lastDate,
      locale: const Locale('es', 'ES'),
    );

    if (picked != null) {
      setState(() {
        _selectedDate = picked;
      });
    }
  }

  Future<void> _selectTime() async {
    final TimeOfDay? picked = await showTimePicker(
      context: context,
      initialTime: TimeOfDay.now(),
    );

    if (picked != null) {
      setState(() {
        _selectedTime = picked;
      });
    }
  }

  Future<void> _createAppointment() async {
    if (_selectedDate == null || _selectedTime == null) {
      setState(() {
        _errorMessage = 'Por favor selecciona fecha y hora';
      });
      return;
    }

    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final userEmail = await StorageService.getUserEmail();
      if (userEmail == null) {
        throw Exception('No se encontró el email del usuario');
      }

      final appointmentDateTime = DateTime(
        _selectedDate!.year,
        _selectedDate!.month,
        _selectedDate!.day,
        _selectedTime!.hour,
        _selectedTime!.minute,
      );

      final appointmentData = CreateAppointmentData(
        userEmail: userEmail,
        serviceName: widget.service.name,
        appointmentDate: appointmentDateTime.toIso8601String(),
      );

      await AppointmentService.createAppointment(appointmentData);

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Cita agendada exitosamente'),
            backgroundColor: Colors.green,
          ),
        );

        Navigator.of(context).pushAndRemoveUntil(
          MaterialPageRoute(builder: (_) => const HomeScreen()),
          (route) => false,
        );
      }
    } catch (e) {
      setState(() {
        _errorMessage = e.toString().replaceAll('Exception: ', '');
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Agendar Cita'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Card(
              elevation: 2,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      widget.service.name,
                      style: const TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      widget.service.category,
                      style: TextStyle(
                        color: Colors.grey[600],
                        fontSize: 14,
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      widget.service.description,
                      style: const TextStyle(fontSize: 14),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 32),
            if (_errorMessage != null)
              Container(
                padding: const EdgeInsets.all(12),
                margin: const EdgeInsets.only(bottom: 16),
                decoration: BoxDecoration(
                  color: Colors.red[50],
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: Colors.red[300]!),
                ),
                child: Row(
                  children: [
                    Icon(Icons.error_outline, color: Colors.red[700]),
                    const SizedBox(width: 8),
                    Expanded(
                      child: Text(
                        _errorMessage!,
                        style: TextStyle(color: Colors.red[700]),
                      ),
                    ),
                  ],
                ),
              ),
            Card(
              elevation: 1,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
              child: ListTile(
                leading: const Icon(Icons.calendar_today),
                title: const Text('Fecha'),
                subtitle: Text(
                  _selectedDate != null
                      ? DateFormat('EEEE, d MMMM y', 'es_ES')
                          .format(_selectedDate!)
                      : 'Selecciona una fecha',
                  style: TextStyle(
                    color: _selectedDate != null
                        ? Colors.black
                        : Colors.grey[600],
                  ),
                ),
                trailing: const Icon(Icons.arrow_forward_ios, size: 16),
                onTap: _selectDate,
              ),
            ),
            const SizedBox(height: 16),
            Card(
              elevation: 1,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
              child: ListTile(
                leading: const Icon(Icons.access_time),
                title: const Text('Hora'),
                subtitle: Text(
                  _selectedTime != null
                      ? _selectedTime!.format(context)
                      : 'Selecciona una hora',
                  style: TextStyle(
                    color: _selectedTime != null
                        ? Colors.black
                        : Colors.grey[600],
                  ),
                ),
                trailing: const Icon(Icons.arrow_forward_ios, size: 16),
                onTap: _selectTime,
              ),
            ),
            const SizedBox(height: 32),
            ElevatedButton(
              onPressed: _isLoading ? null : _createAppointment,
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 16),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
              child: _isLoading
                  ? const SizedBox(
                      height: 20,
                      width: 20,
                      child: CircularProgressIndicator(strokeWidth: 2),
                    )
                  : const Text(
                      'Confirmar Cita',
                      style: TextStyle(fontSize: 16),
                    ),
            ),
          ],
        ),
      ),
    );
  }
}
