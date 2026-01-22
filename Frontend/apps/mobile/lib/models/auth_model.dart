class LoginCredentials {
  final String email;
  final String password;

  LoginCredentials({
    required this.email,
    required this.password,
  });

  Map<String, dynamic> toJson() {
    return {
      'email': email,
      'password': password,
    };
  }
}

class RegisterData {
  final String fullName;
  final String email;
  final String password;

  RegisterData({
    required this.fullName,
    required this.email,
    required this.password,
  });

  Map<String, dynamic> toJson() {
    return {
      'full_name': fullName,
      'email': email,
      'password': password,
    };
  }
}

class AuthResponse {
  final String accessToken;
  final String tokenType;
  final User? user;

  AuthResponse({
    required this.accessToken,
    required this.tokenType,
    this.user,
  });

  factory AuthResponse.fromJson(Map<String, dynamic> json) {
    return AuthResponse(
      accessToken: json['access_token'] ?? '',
      tokenType: json['token_type'] ?? 'Bearer',
      user: json['user'] != null ? User.fromJson(json['user']) : null,
    );
  }
}

class User {
  final String id;
  final String email;
  final String fullName;
  final String role;
  final String? userType;

  User({
    required this.id,
    required this.email,
    required this.fullName,
    required this.role,
    this.userType,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id']?.toString() ?? '',
      email: json['email'] ?? '',
      fullName: json['full_name'] ?? '',
      role: json['role'] ?? 'USUARIO',
      userType: json['user_type'],
    );
  }

  bool get isAdmin => role == 'ADMIN';
}
