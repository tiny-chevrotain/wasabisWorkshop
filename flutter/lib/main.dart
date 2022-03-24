import 'dart:math';

import 'package:flutter/material.dart';
import 'package:myapp/colors.dart';
import 'package:myapp/wasabia_components.dart';
import 'package:myapp/wasabia_list_page.dart';

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


final wasabias_json = [];

List<Wasabia> wasabia_array = wasabias_json
    .map((wasabia) => new Wasabia(
          id: wasabia['id'] as String,
          name: wasabia['name'] as String,
          image: wasabia['image'] as String,
          votes: wasabia['votes'] as int,
          songs: wasabia['songs'] as int,
        ))
    .toList();

// void main() {
//   runApp(MyApp());
// }
