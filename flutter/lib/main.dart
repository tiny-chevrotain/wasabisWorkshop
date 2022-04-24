import 'package:flutter/material.dart';
import 'package:myapp/global_variables.dart';
import 'package:myapp/home_page.dart';
import 'package:myapp/login_page.dart';
import 'package:myapp/spotify_auth_page.dart';
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
        '/login': (context) => LoadLoginSignupPage(),
        '/discover': (context) => LoadDiscoverPage(),
        // '/spotify-auth': (context) => LoadSpotifyAuthPage(),
      },
      onGenerateRoute: (settings) {
        // If you push the PassArguments route
        if (settings.name != null) {
          print(settings.name);
          //in your example: settings.name = "/post?id=123"
          final settingsUri = Uri.parse(settings.name!);
          if (settingsUri.path == '/spotify-auth') {
            final _code = settingsUri.queryParameters['code'];
            print(_code); //will print "123"
            return MaterialPageRoute(
              builder: (context) {
                return LoadSpotifyAuthPage(
                  code: _code!,
                );
              },
            );
          }
        }
        // The code only supports
        // PassArgumentsScreen.routeName right now.
        // Other values need to be implemented if we
        // add them. The assertion here will help remind
        // us of that higher up in the call stack, since
        // this assertion would otherwise fire somewhere
        // in the framework.
        assert(false, 'Need to implement ${settings.name}');
        return null;
      },
      home: HomePage(),
    );
  }
}
