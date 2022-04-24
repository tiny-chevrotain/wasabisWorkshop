import 'package:flutter_secure_storage/flutter_secure_storage.dart';

//todo: restructure class!!
class Credentials {
  final _storage = new FlutterSecureStorage();
  String? _stored_token;

  Future<String?> get() async {
    _stored_token = await _storage.read(key: 'token');
    return _convert(_stored_token);
  }

  remove() async {
    await _storage.deleteAll();
  }

  update(String token) async {
    await _storage.write(key: 'token', value: token);
  }

  Future<String?> get_local() async {
    return _convert(_stored_token);
  }

  String? _convert(String? token) {
    return (token == null) ? null : "token $token";
  }
}
