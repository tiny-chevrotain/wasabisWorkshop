import 'package:flutter/material.dart';
import 'package:myapp/global_variables.dart';
import 'package:myapp/login_page.dart';
import 'package:myapp/url_strategy.dart';
import 'package:myapp/wasabia_list_page.dart';

void main() {
  usePathUrlStrategy();
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      debugShowCheckedModeBanner: false,
      theme: new ThemeData(
        scaffoldBackgroundColor: colour_bckgrnd,
        brightness: Brightness.dark,
      ),
      routes: {
        // 'login': (context) => LoginSignupPage(),
        '/discover': (context) => LoadDiscoverPage(),
      },
      home: LoadLoginSignupPage(),
    );
  }
}
