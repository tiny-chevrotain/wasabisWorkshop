import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';
import 'package:myapp/credentials.dart';
import 'dart:math';

import 'package:myapp/wasabia_components.dart';

final Color color_1 = Color(0xffECECEC);
final Color color_2 = Color(0xff262626);
final Color color_3 = Color(0xffC9D09A);
final Color color_4 = Color(0xff4A4A4A);
final Color color_5 = Color(0xff888888);
final Color colour_bckgrnd = Color(0xff1B1B1B);
final String root_url = "127.0.0.1:8000";
var client = http.Client();

final String error_image =
    'https://i.pinimg.com/564x/69/d1/aa/69d1aadc446c35120da7e9162f33bbc0.jpg';
// final Color color_6 = Color(0xECECEC);

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

Credentials credentials = new Credentials();
