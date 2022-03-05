import 'package:flutter/material.dart';
import 'package:myapp/wasabia_components.dart';

class WasabiaPage extends StatelessWidget {
  const WasabiaPage({
    Key? key,
    required this.id,
    required this.songs,
  }) : super(key: key);

  final String id;
  final List<Song> songs;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: ListView.builder(
          itemCount: songs.length,
          padding: const EdgeInsets.all(20.0),
          shrinkWrap: true,
          itemBuilder: (BuildContext context, int index) {
            return WasabiaSong(
                value: songs[index].votes,
                init_change: songs[index].user_vote,
                song: songs[index].name,
                artist: songs[index].artist,
                index: index + 1);
          }),
    );
  }
}
