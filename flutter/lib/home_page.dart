import 'package:flutter/material.dart';
import 'package:myapp/global_variables.dart';

class HomePage extends StatelessWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.all(50.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            Padding(
              padding: const EdgeInsets.fromLTRB(0, 8.0, 8.0, 8.0),
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(
                  primary: color_5,
                ),
                child: Text(
                  'Login',
                  style: TextStyle(
                    fontSize: 20.0,
                  ),
                ),
                onPressed: () {
                  Navigator.of(context).pushNamed(
                    '/login',
                  );
                },
              ),
            ),
            Padding(
              padding: const EdgeInsets.fromLTRB(0, 8.0, 8.0, 8.0),
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(
                  primary: color_4,
                ),
                child: Text(
                  'Discover',
                  style: TextStyle(fontSize: 20.0),
                ),
                onPressed: () {
                  Navigator.of(context).pushNamed(
                    '/discover',
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}
