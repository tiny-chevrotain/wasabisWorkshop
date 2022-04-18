import 'package:flutter/material.dart';
import 'package:myapp/api_functions.dart';
import 'package:myapp/global_variables.dart';
import 'package:myapp/load_page.dart';

// check_logged_in(BuildContext context)

class LoadLoginSignupPage extends StatelessWidget {
  const LoadLoginSignupPage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return FutureBuilder(
      future: auto_login(context),
      builder: (BuildContext context, AsyncSnapshot snapshot) {
        if (snapshot.hasData && snapshot.data == false) {
          return LoginSignupPage();
        }
        return LoadingPage();
      },
    );
  }
}

class LoginSignupPage extends StatefulWidget {
  const LoginSignupPage({Key? key}) : super(key: key);

  @override
  State<LoginSignupPage> createState() => _LoginSignupPageState();
}

class _LoginSignupPageState extends State<LoginSignupPage> {
  TextEditingController _email_field = TextEditingController();
  TextEditingController _password_field = TextEditingController();
// LoadingPage

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.all(50.0),
        child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: <Widget>[
              TextField(
                decoration: InputDecoration(
                  hintText: "example@gmail.com",
                  labelText: "Email",
                ),
                controller: _email_field,
              ),
              TextField(
                obscureText: true,
                decoration: InputDecoration(
                  labelText: "Password",
                  hintText: "At least 6 characters",
                ),
                controller: _password_field,
              ),
              Row(
                children: <Widget>[
                  Padding(
                    padding: const EdgeInsets.fromLTRB(0, 8.0, 8.0, 8.0),
                    child: ElevatedButton(
                      style: ElevatedButton.styleFrom(
                        primary: color_5,
                      ),
                      child: Text(
                        'SignUp',
                        style: TextStyle(
                          fontSize: 20.0,
                        ),
                      ),
                      onPressed: () {
                        authenticate(
                            context, _email_field.text, _password_field.text,
                            signup: true);
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
                        'Login',
                        style: TextStyle(fontSize: 20.0),
                      ),
                      onPressed: () {
                        authenticate(
                            context, _email_field.text, _password_field.text);
                      },
                    ),
                  ),
                ],
              ),
            ]),
      ),
    );
  }
}
