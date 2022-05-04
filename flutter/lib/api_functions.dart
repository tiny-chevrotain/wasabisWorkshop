import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:myapp/add_songs_page.dart';
import 'package:myapp/global_variables.dart';
import 'package:myapp/personalise_page.dart';
import 'package:myapp/wasabia_components.dart';
import 'package:url_launcher/url_launcher.dart';

// https://stackoverflow.com/questions/45031499/how-to-get-unique-device-id-in-flutter#:~:text=7-,Update%201/3/2021,-%3A%20The%20recommended%20way
// leave unique device bc time lol

Future<bool> authenticate(BuildContext context, String email, String password,
    {bool signup = false}) async {
  String page = signup ? 'workshop/signup/' : 'workshop/login/';
  var body = {'email': email, 'password': password};
  if (signup) body['name'] = email;

  var response = await client.post(
    Uri.http(root_url, page),
    body: body,
  );
  var decodedResponse = jsonDecode(utf8.decode(response.bodyBytes)) as Map;

  if (response.statusCode == 200) {
    print(decodedResponse);
    await credentials.update(decodedResponse['token']);

    if (decodedResponse['spotify_auth'] == 'false') {
      final Uri _url = Uri.parse(decodedResponse['url']);
      if (!await launchUrl(
        _url,
        webOnlyWindowName: '_self',
      )) throw 'Could not launch $_url';
      return false;
    } else {
      Navigator.of(context).pushNamed(
        '/discover',
      );
      return true;
    }
  } else {
    await credentials.remove();
    return false;
  }
}

Future<bool> auto_login(BuildContext context) async {
  String page = 'workshop/token-login/';
  var headers = await get_token_header();
  if (headers != null) {
    var response = await client.post(
      Uri.http(root_url, page),
      headers: headers,
    );
    var decodedResponse = jsonDecode(utf8.decode(response.bodyBytes)) as Map;
    if (response.statusCode == 200) {
      print(decodedResponse);
      Navigator.of(context).pushNamed(
        '/discover',
      );
      return true;
    }
  }
  return false;
}

Future<Map<String, String>?> get_token_header() async {
  String? token = await credentials.get();
  return (token != null) ? {'Authorization': token} : null;
}

logout(BuildContext context) async {
  await credentials.remove();
  Navigator.popUntil(context, ModalRoute.withName('/login'));
}

Future<bool> authenticate_code(String code) async {
  String page = 'workshop/spotify-create-token/';
  var headers = await get_token_header();
  if (headers != null) {
    var response = await client.post(
      Uri.http(root_url, page),
      headers: headers,
      body: {'code': code},
    );
    var decodedResponse = jsonDecode(utf8.decode(response.bodyBytes)) as Map;
    if (response.statusCode == 200) {
      print(decodedResponse);
      return true;
    }
  }
  return false;
}

Future<Map<String, dynamic>?> get_info(
    {required String path, Map<String, String>? query}) async {
  String page = 'workshop/$path';
  var headers = await get_token_header();
  print("We got the headers");
  if (headers != null) {
    var response = await client.get(
      Uri.http(root_url, page, query),
      headers: headers,
    );
    var decodedResponse = jsonDecode(utf8.decode(response.bodyBytes)) as Map;
    if (response.statusCode == 200) {
      return decodedResponse as Map<String, dynamic>;
    }
  }
  return null;
}

Future<Map<String, dynamic>?> put_info(
    {required String path, Map<String, dynamic>? body}) async {
  String page = 'workshop/$path';
  var headers = await get_token_header();
  if (headers != null) {
    var response = await client.put(
      Uri.http(root_url, page),
      headers: headers,
      body: body,
    );
    var decodedResponse = jsonDecode(utf8.decode(response.bodyBytes)) as Map;
    if (response.statusCode == 200) {
      return decodedResponse as Map<String, dynamic>;
    }
  }
  return null;
}

Future<Map<String, dynamic>?> post_info(
    {required String path, Map<String, dynamic>? body}) async {
  String page = 'workshop/$path';
  var headers = await get_token_header();
  if (headers != null) {
    var response = await client.post(
      Uri.http(root_url, page),
      headers: headers,
      body: body,
    );
    var decodedResponse = jsonDecode(utf8.decode(response.bodyBytes)) as Map;
    if (response.statusCode == 200) {
      return decodedResponse as Map<String, dynamic>;
    }
  }
  return null;
}

Future<List<dynamic>?> get_wasabia_list() async {
  Map<String, dynamic>? wasabia_list_response = await get_info(
    path: 'get-wasabia-list/',
  );
  if (wasabia_list_response != null) {
    print(wasabia_list_response['wasabias'].runtimeType);
    return wasabia_list_response['wasabias'];
  }
  return null;
}

Future<List<Wasabia>> getDiscover(String userid) async {
  await credentials.get();
  var wasabias_json = await get_wasabia_list();
  List<Wasabia> wasabia_array = wasabias_json!
      .map((wasabia) => new Wasabia(
            id: wasabia['id'] as int,
            name: wasabia['name'] as String,
            image: (wasabia['image'] ?? error_image) as String,
            votes: (wasabia['votes']['votes_total__sum'] ?? 0) as int,
            songs: wasabia['song_count'] as int,
          ))
      .toList();
  print(wasabia_array[0].votes);
  print(wasabia_array[0].songs);
  print(wasabia_array);
  return wasabia_array;
}

Future<List<Song>?> get_wasabia(int wasabia_id) async {
  var wasabia_response = await get_info(
    path: 'get-wasabia',
    query: {'id': '$wasabia_id'},
  );
  List<dynamic> wasabia_scores = wasabia_response!['wasabia']['scores'];
  List<Song> songs = wasabia_scores
      .map((song) => new Song(
            id: song['song']['id'] as String,
            name: song['song']['name'] as String,
            artist: concatenate(song['song']['artists'], 'name', ', '),
            votes: song['votes_total'] as int,
            user_vote: (song['upvotes_count'] as int) -
                (song['downvotes_count'] as int),
            image_url: song['song']['image_64_url'] as String,
          ))
      .toList();
  return songs;
}

Future<bool> vote_on_song(String song_id, int wasabia_id, int vote) async {
  Map<dynamic, dynamic>? response = await put_info(
    path: 'song-vote/',
    body: {
      'vote': '$vote',
      'song_id': song_id,
      'wasabia_id': '$wasabia_id',
    },
  );
  if (response!['score']['votes_total'] == vote) {
    return true;
  }
  return false;
}

Future<List<SongToAdd>?> get_saved_songs() async {
  var wasabia_response = await get_info(
    path: 'get-user-saved-songs/',
  );
  List<dynamic> wasabia_scores = wasabia_response!['saved_songs'];
  List<SongToAdd> songs = wasabia_scores
      .map((song) => new SongToAdd(
            id: song['track']['id'] as String,
            name: song['track']['name'] as String,
            artists: song['track']['artists'] as List<dynamic>,
            image_640_url: song['track']['album']['images'][0]['url'] as String,
            image_300_url: song['track']['album']['images'][1]['url'] as String,
            image_64_url: song['track']['album']['images'][2]['url'] as String,
          ))
      .toList();
  return songs;
}

Future<List<Song>?> add_songs_to_wasabia(
    {required List<SongToAdd>? songs_to_add, required int wasabia_id}) async {
  var selected_songs = <SongToAdd>[];
  if (songs_to_add != null) {
    for (var i = 0; i < songs_to_add.length; i++) {
      if (songs_to_add[i].selected) {
        selected_songs.add(songs_to_add[i]);
      }
    }
    if (selected_songs.isNotEmpty) {
      List<Map<String, dynamic>> songs = selected_songs
          .map((song) => {
                "id": song.id,
                "name": song.name,
                "artists": song.artists,
                "image_640_url": song.image_640_url,
                "image_300_url": song.image_300_url,
                "image_64_url": song.image_64_url,
              })
          .toList();
      String? token = await credentials.get();

      var response = await client.put(
        Uri.http(root_url, 'workshop/add-songs/'),
        body: jsonEncode({'songs': songs, 'wasabia_id': wasabia_id}),
        headers: {
          'Authorization': token!,
          "content-type": "application/json",
          "accept": "application/json",
        },
      );
      if (response.statusCode == 200) {
        return get_wasabia(wasabia_id);
      }
    }
  }
  return null;
}

Future<List<RecommendedSong>?> get_recommendations(
    {required int wasabia_id}) async {
  var response = await get_info(
      path: 'get-recommendations/', query: {'wasabia_id': '$wasabia_id'});

  List<RecommendedSong> songs = <RecommendedSong>[];
  for (var song in response!['recommendations']) {
    songs.add(new RecommendedSong(
      id: song['id'] as String,
      name: song['name'] as String,
      artist: concatenate(song['artists'], 'name', ', '),
      image_url: song['album']['images'][1]['url'] as String,
      sim: song['sim'] as double,
    ));
  }
  return songs;
}

Future<List<RecommendedSong>?> get_recommendations_test(
    {required int wasabia_id}) async {
  var wasabia_response = await get_info(
    path: 'get-wasabia',
    query: {'id': '$wasabia_id'},
  );
  List<dynamic> wasabia_scores = wasabia_response!['wasabia']['scores'];
  List<RecommendedSong> songs = wasabia_scores
      .map((song) => new RecommendedSong(
            id: song['song']['id'] as String,
            name: song['song']['name'] as String,
            artist: concatenate(song['song']['artists'], 'name', ', '),
            image_url: song['song']['image_64_url'] as String,
            sim: 1.0,
          ))
      .toList();
  return songs;
}

Future create_wasabia(
    {required String name, required BuildContext context}) async {
  Map<dynamic, dynamic>? response = await post_info(
    path: 'create-wasabia/',
    body: {
      'name': name,
      'description': '',
    },
  );
  Navigator.pop(context);
}

String concatenate(List<dynamic> map_to_concat, String key, String connector) {
  String concatenated_string = '';
  for (var i = 0; i < map_to_concat.length; i++) {
    concatenated_string +=
        ((i == 0) ? '' : connector) + (map_to_concat[i][key]! as String);
  }
  return concatenated_string;
}
