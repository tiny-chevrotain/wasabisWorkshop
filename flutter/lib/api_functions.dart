import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:myapp/global_variables.dart';
import 'package:myapp/wasabia_components.dart';

Future<bool> authenticate(BuildContext context, String email, String password,
    {bool signup = false}) async {
  String page = signup ? 'workshop/signup/' : 'workshop/login/';
  var body = {'email': email, 'password': password};
  if (signup) body['name'] = email;

  await check_logged_in(body);

  var response = await client.post(
    Uri.http(root_url, page),
    body: body,
  );

  if (response.statusCode == 200) {
    var decodedResponse = jsonDecode(utf8.decode(response.bodyBytes)) as Map;
    await credentials.update(email, password);
    Navigator.of(context).pushNamed(
      '/discover',
    );
    return true;
  } else {
    var decodedResponse = jsonDecode(utf8.decode(response.bodyBytes)) as Map;
    await credentials.remove();
    return false;
  }
}

Future<bool> auto_login(BuildContext context) async {
  var _credentials = await credentials.get();
  if (_credentials != null) {
    return await authenticate(
        context, _credentials['email']!, _credentials['password']!);
  }
  return false;
}

check_logged_in(var body) async {
  String page = 'workshop/is-logged-in/';
  await credentials.remove();
  var response = await client.post(
    Uri.http(root_url, page),
    body: body,
  );

  if (response.statusCode == 200) {
    var decodedResponse = jsonDecode(utf8.decode(response.bodyBytes)) as Map;
    print(decodedResponse);
  } else {
    var decodedResponse = jsonDecode(utf8.decode(response.bodyBytes)) as Map;
    print(decodedResponse);
  }
}

logout(BuildContext context) async {
  String page = 'workshop/logout/';
  await credentials.remove();
  var response = await client.post(
    Uri.http(root_url, page),
  );

  if (response.statusCode == 200) {
    var decodedResponse = jsonDecode(utf8.decode(response.bodyBytes)) as Map;
    Navigator.pop(context);
  } else {
    var decodedResponse = jsonDecode(utf8.decode(response.bodyBytes)) as Map;
  }
}

Future<List<Wasabia>> getDiscover(String userid) async {
  await credentials.get();
  return wasabia_array;
}
