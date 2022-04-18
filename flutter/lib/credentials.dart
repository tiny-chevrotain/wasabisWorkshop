import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class Credentials {
  final _storage = new FlutterSecureStorage();
  String? _stored_email;
  String? _stored_password;

  Future<Map<String, String>?> get() async {
    _stored_email = await _storage.read(key: 'email');
    _stored_password = await _storage.read(key: 'password');

    if ((_stored_email != null) && (_stored_password != null)) {
      return {
        'email': _stored_email!,
        'password': _stored_password!,
      };
    }
    await remove();
    return null;
  }

  remove() async {
    await _storage.deleteAll();
  }

  update(String email, String password) async {
    await _storage.write(key: 'email', value: email);
    await _storage.write(key: 'password', value: password);
  }

  Future<String?> get_email() async {
    _stored_email = await _storage.read(key: 'email');
    return _stored_email;
  }
}
