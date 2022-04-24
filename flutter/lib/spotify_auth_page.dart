import 'package:flutter/material.dart';
import 'package:myapp/api_functions.dart';
import 'package:myapp/global_variables.dart';
import 'package:myapp/load_page.dart';

// check_logged_in(BuildContext context)

class LoadSpotifyAuthPage extends StatelessWidget {
  final String code;

  const LoadSpotifyAuthPage({
    Key? key,
    required this.code,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return FutureBuilder(
      future: authenticate_code(code),
      builder: (BuildContext context, AsyncSnapshot snapshot) {
        if (snapshot.hasData) {
          return SpotifyAuthPage();
        }
        return LoadingPage();
      },
    );
  }
}

class SpotifyAuthPage extends StatelessWidget {
  const SpotifyAuthPage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.all(50.0),
        child: Text(":P IT WORKED!! AFTER SO LONG IT FINALLY WORKED AAHHH"),
      ),
    );
  }
}
