import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class StorageService {
  static const FlutterSecureStorage _storage = FlutterSecureStorage();
  static const String _tokenKey = 'jwt_token';
  static const String _userEmailKey = 'user_email';

  static Future<void> saveToken(String token) async {
    await _storage.write(key: _tokenKey, value: token);
  }

  static Future<String?> getToken() async {
    return await _storage.read(key: _tokenKey);
  }

  static Future<void> deleteToken() async {
    await _storage.delete(key: _tokenKey);
  }

  static Future<void> saveUserEmail(String email) async {
    await _storage.write(key: _userEmailKey, value: email);
  }

  static Future<String?> getUserEmail() async {
    return await _storage.read(key: _userEmailKey);
  }

  static Future<void> clearAll() async {
    await _storage.deleteAll();
  }
}
