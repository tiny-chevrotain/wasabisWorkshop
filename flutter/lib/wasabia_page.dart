import 'package:flutter/material.dart';
import 'package:myapp/add_songs_page.dart';
import 'package:myapp/api_functions.dart';
import 'package:myapp/global_variables.dart';
import 'package:myapp/load_page.dart';
import 'package:myapp/personalise_page.dart';
import 'package:myapp/wasabia_components.dart';

class LoadWasabiaPage extends StatefulWidget {
  const LoadWasabiaPage({
    Key? key,
    required this.id,
  }) : super(key: key);
  final int id;

  @override
  State<LoadWasabiaPage> createState() => _LoadWasabiaPageState();
}

class _LoadWasabiaPageState extends State<LoadWasabiaPage> {
  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder(
      future: get_wasabia(widget.id),
      builder: (BuildContext context, AsyncSnapshot snapshot) {
        if (snapshot.hasData) {
          return WasabiaPage(id: widget.id, songs: snapshot.data);
        }
        return LoadingPage();
      },
    );
  }
}

class WasabiaPage extends StatefulWidget {
  const WasabiaPage({
    Key? key,
    required this.id,
    required this.songs,
  }) : super(key: key);

  final int id;
  final List<Song> songs;
  @override
  State<WasabiaPage> createState() => _WasabiaPageState();
}

class _WasabiaPageState extends State<WasabiaPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.fromLTRB(0, 8.0, 8.0, 8.0),
            child: ElevatedButton(
              style: ElevatedButton.styleFrom(
                primary: color_4,
              ),
              child: Text(
                'Logout',
                style: TextStyle(fontSize: 20.0),
              ),
              onPressed: () {
                logout(context);
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
                'Add new songs',
                style: TextStyle(fontSize: 20.0),
              ),
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => LoadSongs(wasabia_id: widget.id),
                  ),
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
                'Personalise',
                style: TextStyle(fontSize: 20.0),
              ),
              onPressed: () async {
                print("Should literally only be doing this");
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => LoadPersonalisePage(id: widget.id),
                  ),
                );
              },
            ),
          ),
          Expanded(
            child: ListView.builder(
              itemCount: widget.songs.length,
              padding: const EdgeInsets.all(20.0),
              shrinkWrap: true,
              itemBuilder: (BuildContext context, int index) {
                return WasabiaSong(
                  value:
                      widget.songs[index].votes - widget.songs[index].user_vote,
                  init_change: widget.songs[index].user_vote,
                  wasabia_id: widget.id,
                  song_id: widget.songs[index].id,
                  song_name: widget.songs[index].name,
                  artist: widget.songs[index].artist,
                  image_url: widget.songs[index].image_url,
                  index: index + 1,
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
