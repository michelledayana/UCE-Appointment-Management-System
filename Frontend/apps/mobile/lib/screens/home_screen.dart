import 'package:flutter/material.dart';
import '../services/auth_service.dart';
import '../services/storage_service.dart';
import 'login_screen.dart';
import 'services_screen.dart';
import '../services/appointment_service.dart';
import '../models/appointment_model.dart';
import 'package:intl/intl.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  List<Appointment> _appointments = [];
  bool _isLoading = true;
  String? _userEmail;
  int _currentIndex = 0;

  @override
  void initState() {
    super.initState();
    _loadUserEmail();
    _loadAppointments();
  }

  Future<void> _loadUserEmail() async {
    final email = await StorageService.getUserEmail();
    setState(() {
      _userEmail = email;
    });
  }

  Future<void> _loadAppointments() async {
    setState(() {
      _isLoading = true;
    });

    try {
      final appointments = await AppointmentService.getMyAppointments();
      setState(() {
        _appointments = appointments;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _isLoading = false;
      });
    }
  }

  Future<void> _handleLogout() async {
    await AuthService.logout();
    if (mounted) {
      Navigator.of(context).pushAndRemoveUntil(
        MaterialPageRoute(builder: (_) => const LoginScreen()),
        (route) => false,
      );
    }
  }

  Widget _buildHomeTab() {
    return RefreshIndicator(
      onRefresh: _loadAppointments,
      child: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _appointments.isEmpty
              ? Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(Icons.calendar_today_outlined,
                          size: 64, color: Colors.grey[400]),
                      const SizedBox(height: 16),
                      Text(
                        'No tienes citas agendadas',
                        style: TextStyle(color: Colors.grey[600]),
                      ),
                    ],
                  ),
                )
              : ListView.builder(
                  padding: const EdgeInsets.all(16),
                  itemCount: _appointments.length,
                  itemBuilder: (context, index) {
                    final appointment = _appointments[index];
                    final date = DateTime.tryParse(appointment.appointmentDate);
                    return Card(
                      margin: const EdgeInsets.only(bottom: 12),
                      elevation: 2,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Padding(
                        padding: const EdgeInsets.all(16),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                Expanded(
                                  child: Text(
                                    appointment.serviceName,
                                    style: const TextStyle(
                                      fontSize: 18,
                                      fontWeight: FontWeight.bold,
                                    ),
                                  ),
                                ),
                                Container(
                                  padding: const EdgeInsets.symmetric(
                                      horizontal: 8, vertical: 4),
                                  decoration: BoxDecoration(
                                    color: _getStatusColor(appointment.status)
                                        .withOpacity(0.2),
                                    borderRadius: BorderRadius.circular(12),
                                  ),
                                  child: Text(
                                    _getStatusText(appointment.status),
                                    style: TextStyle(
                                      color: _getStatusColor(appointment.status),
                                      fontSize: 12,
                                      fontWeight: FontWeight.w500,
                                    ),
                                  ),
                                ),
                              ],
                            ),
                            const SizedBox(height: 12),
                            if (date != null) ...[
                              Row(
                                children: [
                                  Icon(Icons.calendar_today,
                                      size: 16, color: Colors.grey[600]),
                                  const SizedBox(width: 8),
                                  Text(
                                    DateFormat('EEEE, d MMMM y', 'es_ES')
                                        .format(date),
                                    style: TextStyle(
                                      color: Colors.grey[700],
                                      fontSize: 14,
                                    ),
                                  ),
                                ],
                              ),
                              const SizedBox(height: 8),
                              Row(
                                children: [
                                  Icon(Icons.access_time,
                                      size: 16, color: Colors.grey[600]),
                                  const SizedBox(width: 8),
                                  Text(
                                    DateFormat('HH:mm').format(date),
                                    style: TextStyle(
                                      color: Colors.grey[700],
                                      fontSize: 14,
                                    ),
                                  ),
                                ],
                              ),
                            ],
                            const SizedBox(height: 8),
                            Row(
                              children: [
                                Icon(Icons.attach_money,
                                    size: 16, color: Colors.grey[600]),
                                const SizedBox(width: 8),
                                Text(
                                  '\$${appointment.price.toStringAsFixed(2)}',
                                  style: TextStyle(
                                    color: Colors.grey[700],
                                    fontSize: 14,
                                    fontWeight: FontWeight.w500,
                                  ),
                                ),
                              ],
                            ),
                          ],
                        ),
                      ),
                    );
                  },
                ),
    );
  }

  Color _getStatusColor(String status) {
    switch (status.toUpperCase()) {
      case 'SCHEDULED':
        return Colors.blue;
      case 'COMPLETED':
        return Colors.green;
      case 'CANCELLED':
        return Colors.red;
      default:
        return Colors.grey;
    }
  }

  String _getStatusText(String status) {
    switch (status.toUpperCase()) {
      case 'SCHEDULED':
        return 'Programada';
      case 'COMPLETED':
        return 'Completada';
      case 'CANCELLED':
        return 'Cancelada';
      default:
        return status;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Mis Citas'),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: _handleLogout,
            tooltip: 'Cerrar sesión',
          ),
        ],
      ),
      body: IndexedStack(
        index: _currentIndex,
        children: [
          _buildHomeTab(),
          const ServicesScreen(),
        ],
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        onTap: (index) {
          setState(() {
            _currentIndex = index;
          });
        },
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.home),
            label: 'Inicio',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.list),
            label: 'Servicios',
          ),
        ],
      ),
    );
  }
}
