import 'package:flutter/material.dart';
import 'package:myapp/api_functions.dart';
import 'package:myapp/global_variables.dart';

class CreateWasabiaPage extends StatefulWidget {
  const CreateWasabiaPage({Key? key}) : super(key: key);

  @override
  State<CreateWasabiaPage> createState() => _CreateWasabiaPageState();
}

class _CreateWasabiaPageState extends State<CreateWasabiaPage> {
  TextEditingController _name_field = TextEditingController();
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
                  hintText: "Wasabia name",
                  labelText: "Name",
                ),
                controller: _name_field,
              ),
              Row(
                children: <Widget>[
                  Padding(
                    padding: const EdgeInsets.fromLTRB(0, 8.0, 8.0, 8.0),
                    child: ElevatedButton(
                      style: ElevatedButton.styleFrom(
                        primary: color_4,
                      ),
                      child: Text(
                        'Create',
                        style: TextStyle(fontSize: 20.0),
                      ),
                      onPressed: () {
                        create_wasabia(
                          context: context,
                          name: _name_field.text,
                        );
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
