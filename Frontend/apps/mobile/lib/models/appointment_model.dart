class Appointment {
  final String id;
  final String userEmail;
  final String serviceName;
  final String appointmentDate;
  final double price;
  final String status;
  final String? createdAt;
  final String? updatedAt;

  Appointment({
    required this.id,
    required this.userEmail,
    required this.serviceName,
    required this.appointmentDate,
    required this.price,
    required this.status,
    this.createdAt,
    this.updatedAt,
  });

  factory Appointment.fromJson(Map<String, dynamic> json) {
    return Appointment(
      id: json['id']?.toString() ?? '',
      userEmail: json['user_email'] ?? '',
      serviceName: json['service_name'] ?? '',
      appointmentDate: json['appointment_date'] ?? '',
      price: (json['price'] ?? 0).toDouble(),
      status: json['status'] ?? 'SCHEDULED',
      createdAt: json['created_at'],
      updatedAt: json['updated_at'],
    );
  }
}

class CreateAppointmentData {
  final String userEmail;
  final String serviceName;
  final String appointmentDate;

  CreateAppointmentData({
    required this.userEmail,
    required this.serviceName,
    required this.appointmentDate,
  });

  Map<String, dynamic> toJson() {
    return {
      'user_email': userEmail,
      'service_name': serviceName,
      'appointment_date': appointmentDate,
    };
  }
}
