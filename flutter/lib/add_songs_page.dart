import 'package:flutter/material.dart';
import 'package:myapp/api_functions.dart';
import 'package:myapp/global_variables.dart';
import 'package:myapp/load_page.dart';
import 'package:myapp/wasabia_page.dart';

class SongToAdd {
  SongToAdd({
    required this.id,
    required this.name,
    required this.artists,
    required this.image_640_url,
    required this.image_300_url,
    required this.image_64_url,
    this.selected = false,
  });

  final String id;
  final String name;
  final List<dynamic> artists;
  final String image_640_url;
  final String image_300_url;
  final String image_64_url;
  bool selected;
}

class SongSelection extends StatelessWidget {
  // final ValueChanged<DateTime> onDateTimeChanged;
  const SongSelection({
    Key? key,
    required this.song_id,
    required this.song_name,
    required this.artist,
    required this.index,
    required this.image_64_url,
    required this.selected,
  }) : super(key: key);
  final int index;
  final String song_id;
  final String song_name;
  final String artist;
  final String image_64_url;
  final bool selected;

  @override
  Widget build(BuildContext context) {
    return Container(
      color: Color.fromARGB(0, 0, 0, 0),
      child: Center(
        child: Container(
          color: (selected) ? color_4 : colour_bckgrnd,
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              Padding(
                padding: const EdgeInsets.all(8.0),
                child: Text("${index}"),
              ),
              Padding(
                padding: const EdgeInsets.all(8.0),
                child: new Container(
                  height: 42.0,
                  width: 42.0,
                  color: Color.fromARGB(255, 54, 222, 244),
                ),
              ),
              Expanded(
                child: Padding(
                  padding: const EdgeInsets.fromLTRB(8, 0, 8, 0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        song_name,
                        style: TextStyle(
                          fontWeight: FontWeight.bold,
                          fontSize: 16.0,
                        ),
                      ),
                      Text(
                        artist,
                        style: TextStyle(
                          fontSize: 10.0,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class LoadSongs extends StatelessWidget {
  const LoadSongs({Key? key, required this.wasabia_id}) : super(key: key);
  final int wasabia_id;

  @override
  Widget build(BuildContext context) {
    return FutureBuilder(
      future: get_saved_songs(),
      builder: (BuildContext context, AsyncSnapshot snapshot) {
        if (snapshot.hasData) {
          return AddSongs(
            songs: snapshot.data,
            wasabia_id: wasabia_id,
          );
        }
        return LoadingPage();
      },
    );
  }
}

class AddSongs extends StatefulWidget {
  const AddSongs({
    Key? key,
    required this.songs,
    required this.wasabia_id,
  }) : super(key: key);
  final List<SongToAdd> songs;
  final int wasabia_id;

  @override
  State<AddSongs> createState() => _AddSongsState();
}

class _AddSongsState extends State<AddSongs> {
  List<SongToAdd>? songs;

  @override
  initState() {
    songs = widget.songs;
    super.initState();
  }

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
                'Add',
                style: TextStyle(fontSize: 20.0),
              ),
              onPressed: () {
                add_songs_to_wasabia(
                  songs_to_add: songs,
                  wasabia_id: widget.wasabia_id,
                );
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) =>
                        LoadWasabiaPage(id: widget.wasabia_id),
                  ),
                );
              },
            ),
          ),
          Expanded(
            child: ListView.builder(
              itemCount: songs!.length,
              padding: const EdgeInsets.all(20.0),
              shrinkWrap: true,
              itemBuilder: (BuildContext context, int index) {
                return GestureDetector(
                  onTap: () {
                    setState(() {
                      songs![index].selected = !songs![index].selected;
                    });
                  },
                  child: SongSelection(
                    song_id: songs![index].id,
                    song_name: songs![index].name,
                    artist: concatenate(songs![index].artists, 'name', ', '),
                    image_64_url: songs![index].image_64_url,
                    index: index + 1,
                    selected: songs![index].selected,
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
