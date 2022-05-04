import 'package:flutter/material.dart';
import 'package:image_network/image_network.dart';
import 'package:myapp/api_functions.dart';
import 'package:myapp/global_variables.dart';
import 'package:myapp/load_page.dart';
import 'package:myapp/wasabia_components.dart';

class RecommendedSong {
  RecommendedSong({
    required this.id,
    required this.name,
    required this.artist,
    required this.sim,
    required this.image_url,
  });

  final String id;
  final String name;
  final String artist;
  final double sim;
  final String image_url;
}

class LoadPersonalisePage extends StatefulWidget {
  const LoadPersonalisePage({
    Key? key,
    required this.id,
  }) : super(key: key);
  final int id;

  @override
  State<LoadPersonalisePage> createState() => _LoadPersonalisePageState();
}

class _LoadPersonalisePageState extends State<LoadPersonalisePage> {
  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder(
      future: get_recommendations(wasabia_id: widget.id),
      builder: (BuildContext context, AsyncSnapshot snapshot) {
        if (snapshot.hasData) {
          return PersonalisePage(id: widget.id, songs: snapshot.data);
        }
        return LoadingPage();
      },
    );
  }
}

class PersonalisePage extends StatelessWidget {
  const PersonalisePage({
    Key? key,
    required this.id,
    required this.songs,
  }) : super(key: key);

  final int id;
  final List<RecommendedSong> songs;

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
          Expanded(
            child: ListView.builder(
              itemCount: songs.length,
              padding: const EdgeInsets.all(20.0),
              shrinkWrap: true,
              itemBuilder: (BuildContext context, int index) {
                return SongRecommendation(
                  wasabia_id: id,
                  song_id: songs[index].id,
                  song_name: songs[index].name,
                  artist: songs[index].artist,
                  image_url: songs[index].image_url,
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

class SongRecommendation extends StatelessWidget {
  const SongRecommendation(
      {Key? key,
      required this.wasabia_id,
      required this.song_id,
      required this.song_name,
      required this.artist,
      required this.index,
      required this.image_url})
      : super(key: key);
  final int index;
  final int wasabia_id;
  final String song_id;
  final String song_name;
  final String artist;
  final String image_url;

  @override
  Widget build(BuildContext context) {
    return Container(
      color: Color.fromARGB(0, 0, 0, 0),
      child: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(
            maxWidth: 700,
          ),
          child: Row(
              mainAxisSize: MainAxisSize.min,
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Flexible(
                  child: Container(
                    alignment: Alignment.centerLeft,
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Padding(
                          padding: const EdgeInsets.all(8.0),
                          child: Text("${index}"),
                        ),
                        Padding(
                          padding: const EdgeInsets.all(8.0),
                          child: ClipRRect(
                            borderRadius: BorderRadius.circular(8.0),
                            child: ImageNetwork(
                              image: image_url,
                              height: 100.0,
                              width: 100.0,
                              fitWeb: BoxFitWeb.cover,
                            ),
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
              ]),
        ),
      ),
    );
  }
}
