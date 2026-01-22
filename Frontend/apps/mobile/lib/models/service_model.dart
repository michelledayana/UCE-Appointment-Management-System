class Service {
  final String id;
  final String name;
  final String category;
  final String description;
  final bool isActive;
  final ServicePrices? prices;

  Service({
    required this.id,
    required this.name,
    required this.category,
    required this.description,
    required this.isActive,
    this.prices,
  });

  factory Service.fromJson(Map<String, dynamic> json) {
    return Service(
      id: json['id']?.toString() ?? '',
      name: json['name'] ?? '',
      category: json['category'] ?? '',
      description: json['description'] ?? '',
      isActive: json['is_active'] ?? true,
      prices: json['prices'] != null
          ? ServicePrices.fromJson(json['prices'])
          : null,
    );
  }
}

class ServicePrices {
  final double? student;
  final double? general;

  ServicePrices({
    this.student,
    this.general,
  });

  factory ServicePrices.fromJson(Map<String, dynamic> json) {
    return ServicePrices(
      student: json['student']?.toDouble(),
      general: json['general']?.toDouble(),
    );
  }
}
