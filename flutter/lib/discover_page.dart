import 'dart:math';

import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';
import 'package:myapp/colors.dart';
import 'package:myapp/wasabia_components.dart';
import 'package:myapp/wasabia_list_page.dart';
import 'package:http/http.dart' as http;

final List<String> images = [
  "https://i.pinimg.com/564x/dd/4a/e9/dd4ae99334a4fd715a61044b9933fcab.jpg",
  "https://i.pinimg.com/564x/a5/d9/2a/a5d92a760dadaa43a59704402abb2ae7.jpg",
  "https://i.pinimg.com/564x/d6/2c/d0/d62cd0f76da332888fdd7061158d55e6.jpg",
  "https://i.pinimg.com/564x/ce/31/ae/ce31ae3810b9ab4085353897a1c2c976.jpg",
  "https://i.pinimg.com/564x/bb/76/01/bb76012ac74f320ebf128675047d9a03.jpg",
  "https://i.pinimg.com/564x/b6/9a/5d/b69a5d789381b54a451f409edd4a819f.jpg",
  "https://i.pinimg.com/564x/ff/79/90/ff7990622fca88fdb52dea298cf16475.jpg",
  "https://i.pinimg.com/564x/70/62/bb/7062bb0fcf04e085dce5cbe245452fb6.jpg",
];
var rand = Random();

final wasabias_json = [
  {
    'id': "",
    'name': "Jazzy songs",
    'image': images[rand.nextInt(images.length)],
    'votes': 9999,
    'songs': 9999,
  },
  {
    'id': "",
    'name': "DnD battle music",
    'image': images[rand.nextInt(images.length)],
    'votes': 9999,
    'songs': 9999,
  },
  {
    'id': "",
    'name': "Songs for a 19th century villain scheming against his enemies",
    'image': images[rand.nextInt(images.length)],
    'votes': 9999,
    'songs': 9999,
  },
  {
    'id': "",
    'name': "Rainy days",
    'image': images[rand.nextInt(images.length)],
    'votes': 9999,
    'songs': 9999,
  },
];

List<Wasabia> wasabia_array = wasabias_json
    .map((wasabia) => new Wasabia(
          id: wasabia['id'] as String,
          name: wasabia['name'] as String,
          image: wasabia['image'] as String,
          votes: wasabia['votes'] as int,
          songs: wasabia['songs'] as int,
        ))
    .toList();

authenticate(BuildContext context, String email, String password) async {
  var headers = {
    'X-CSRFToken':
        'AyjC0bdXAz611Z7gZi2pFHWBtXsYmjv8NdUMT4WtVxarxQWfOsNloE5jukWsxuVD',
    'sessionid': 'o8vd0ovd7ntpqjr2yg8sm3biqjg2wf72',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie':
        'csrftoken=liumkhXZCmMKoQGXn9UFy8d4og2Ro5u4LPA97yHd1P3d6hfKfS1tuRvVArxFvVuZ; sessionid=nc5hr0n1ua099xmi4trygcp1w0p2zpk1'
  };
  var request =
      http.Request('POST', Uri.parse('http://127.0.0.1:8000/workshop/login/'));
  request.bodyFields = {'email': email, 'password': password};
  request.headers.addAll(headers);

  http.StreamedResponse response = await request.send();

  if (response.statusCode == 200) {
    print(await response.stream.bytesToString());
    Navigator.push(
      context,
      MaterialPageRoute(
          builder: (context) => WasabiaListPage(
                wasabias: wasabia_array,
              )),
    );
  } else {
    print(response.reasonPhrase);
  }
}

class DiscoverPage extends StatefulWidget {
  const DiscoverPage({Key? key}) : super(key: key);

  @override
  State<DiscoverPage> createState() => _DiscoverPageState();
}

class _DiscoverPageState extends State<DiscoverPage> {
  TextEditingController _email_field = TextEditingController();
  TextEditingController _password_field = TextEditingController();

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
                            context, _email_field.text, _password_field.text);
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
