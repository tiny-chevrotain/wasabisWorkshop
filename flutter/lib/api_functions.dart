import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:myapp/global_variables.dart';
import 'package:myapp/wasabia_components.dart';
import 'package:url_launcher/url_launcher.dart';

// https://stackoverflow.com/questions/45031499/how-to-get-unique-device-id-in-flutter#:~:text=7-,Update%201/3/2021,-%3A%20The%20recommended%20way
// leave unique device bc time lol

Future<bool> authenticate(BuildContext context, String email, String password,
    {bool signup = false}) async {
  String page = signup ? 'workshop/signup/' : 'workshop/login/';
  var body = {'email': email, 'password': password};
  if (signup) body['name'] = email;

  var response = await client.post(
    Uri.http(root_url, page),
    body: body,
  );
  var decodedResponse = jsonDecode(utf8.decode(response.bodyBytes)) as Map;

  if (response.statusCode == 200) {
    print(decodedResponse);
    await credentials.update(decodedResponse['token']);

    if (decodedResponse['spotify_auth'] == 'false') {
      final Uri _url = Uri.parse(decodedResponse['url']);
      if (!await launchUrl(
        _url,
        webOnlyWindowName: '_self',
      )) throw 'Could not launch $_url';
      return false;
    } else {
      Navigator.of(context).pushNamed(
        '/discover',
      );
      return true;
    }
  } else {
    await credentials.remove();
    return false;
  }
}

Future<bool> auto_login(BuildContext context) async {
  String page = 'workshop/token-login/';
  var headers = await get_token_header();
  if (headers != null) {
    var response = await client.post(
      Uri.http(root_url, page),
      headers: headers,
    );
    var decodedResponse = jsonDecode(utf8.decode(response.bodyBytes)) as Map;
    if (response.statusCode == 200) {
      print(decodedResponse);
      Navigator.of(context).pushNamed(
        '/discover',
      );
      return true;
    }
  }
  return false;
}

Future<Map<String, String>?> get_token_header() async {
  String? token = await credentials.get();
  return (token != null) ? {'Authorization': token} : null;
}

logout(BuildContext context) async {
  await credentials.remove();
  Navigator.pop(context);
}

Future<List<Wasabia>> getDiscover(String userid) async {
  await credentials.get();
  return wasabia_array;
}

Future<bool> authenticate_code(String code) async {
  print(code);
  await credentials.get();
  return true;
}
