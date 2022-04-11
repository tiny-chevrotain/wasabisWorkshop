import 'package:flutter/material.dart';
import 'package:myapp/colors.dart';
import 'package:myapp/discover_page.dart';

void main() {
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
      home: DiscoverPage(),
    );
  }
}
