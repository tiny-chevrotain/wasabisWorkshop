import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:myapp/colors.dart';
import 'package:myapp/wasabia_components.dart';
import 'package:myapp/wasabia_page.dart';
import 'package:image_network/image_network.dart';

//https://codeitoutt.medium.com/how-to-display-anonymous-number-of-images-in-flutter-using-listview-builder-e2e8aaa2fa0a

// final String id;
//   final String name;
//   final String artist;
//   final int votes;
//   final int user_vote;

final songs_json = [
  {
    'id': "",
    'name': "Who Am I",
    'artist': "Michael Wyckoff",
    'votes': 9999,
    'user_vote': 0,
  },
  {
    'id': "",
    'name': "Rusty Cage",
    'artist': "Soundgarden",
    'votes': 9999,
    'user_vote': 0,
  },
  {
    'id': "",
    'name': "tadpoles lullaby",
    'artist': "galen tipton",
    'votes': 9999,
    'user_vote': 0,
  },
  {
    'id': "",
    'name': "Evil Fantasy",
    'artist': "Freddie Dredd",
    'votes': 9999,
    'user_vote': 0,
  },
  {
    'id': "",
    'name': "Turn out the Lamplight",
    'artist': "George Benson",
    'votes': 9999,
    'user_vote': 0,
  },
];

List<Song> songs = songs_json
    .map((song) => new Song(
          id: song['id'] as String,
          name: song['name'] as String,
          artist: song['artist'] as String,
          votes: song['votes'] as int,
          user_vote: song['user_vote'] as int,
        ))
    .toList();

class WasabiaListPage extends StatelessWidget {
  const WasabiaListPage({
    Key? key,
    required this.wasabias,
  }) : super(key: key);

  final List<Wasabia> wasabias;
  final double title_size = 30;
  final double vote_size = 7.5;
  final double meta_size = 20;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: ListView.builder(
        itemCount: wasabias.length,
        itemBuilder: (BuildContext context, int index) {
          return Padding(
            padding: EdgeInsets.all(15.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Padding(
                  padding: const EdgeInsets.only(bottom: 5.0),
                  child: ClipRRect(
                    borderRadius: BorderRadius.circular(8.0),
                    child: ImageNetwork(
                      image: wasabias[index].image,
                      height: 300.0,
                      width: 300.0,
                      fitWeb: BoxFitWeb.cover,
                      onTap: () {
                        Navigator.of(context).push(MaterialPageRoute(
                            builder: (context) => WasabiaPage(
                                  id: wasabias[index].id,
                                  songs: songs,
                                )));
                      },
                    ),
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.only(bottom: 2.0),
                  child: Text(
                    wasabias[index].name,
                    style: TextStyle(
                      color: color_1,
                      fontWeight: FontWeight.bold,
                      fontSize: title_size,
                    ),
                  ),
                ),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: <Widget>[
                    Text(
                      "${wasabias[index].votes}",
                      style: TextStyle(
                        color: color_5,
                        fontWeight: FontWeight.w500,
                        fontSize: meta_size,
                      ),
                    ),
                    Padding(
                      padding: const EdgeInsets.all(3.0),
                      child: Column(
                        children: <Widget>[
                          SizedBox(height: 4),
                          SvgPicture.asset(
                            "assets/icons/buttons/upvote.svg",
                            semanticsLabel: 'Upvote',
                            color: color_1,
                            width: vote_size,
                            height: vote_size,
                          ),
                          SvgPicture.asset(
                            "assets/icons/buttons/downvote.svg",
                            semanticsLabel: 'Downvote',
                            color: color_4,
                            width: vote_size,
                            height: vote_size,
                          ),
                        ],
                      ),
                    ),
                    Text(
                      " ${wasabias[index].songs}",
                      style: TextStyle(
                        color: color_5,
                        fontWeight: FontWeight.w500,
                        fontSize: meta_size,
                      ),
                    ),
                    Padding(
                      padding: const EdgeInsets.all(3.0),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: <Widget>[
                          SizedBox(height: 4),
                          SvgPicture.asset(
                            "assets/icons/buttons/foundation_music.svg",
                            semanticsLabel: 'Song',
                            color: color_4,
                            width: vote_size + 6,
                            height: vote_size + 6,
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}



// class WasabiaElement extends StatelessWidget {
//   const WasabiaElement({
//     Key? key,
//     required this.id,
//     required this.name,
//     required this.image,
//     required this.votes,
//     required this.songs,
//   }) : super(key: key);

//   final String id;
//   final String name;
//   final String image;
//   final int votes;
//   final int songs;

//   final double title_size = 30;
//   final double vote_size = 7.5;
//   final double meta_size = 20;

//   @override
//   Widget build(BuildContext context) {
//     return 
//   }
// }
