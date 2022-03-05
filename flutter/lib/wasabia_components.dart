import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:myapp/colors.dart';

class Wasabia {
  Wasabia({
    required this.id,
    required this.name,
    required this.image,
    required this.votes,
    required this.songs,
  });

  final String id;
  final String name;
  final String image;
  final int votes;
  final int songs;
}

class Song {
  Song({
    required this.id,
    required this.name,
    required this.artist,
    required this.votes,
    required this.user_vote,
  });

  final String id;
  final String name;
  final String artist;
  final int votes;
  final int user_vote;
}

class WasabiaListing extends StatefulWidget {
  const WasabiaListing({Key? key}) : super(key: key);

  @override
  _WasabiaListingState createState() => _WasabiaListingState();
}

class _WasabiaListingState extends State<WasabiaListing> {
  @override
  Widget build(BuildContext context) {
    return Container();
  }
}

class WasabiaSong extends StatefulWidget {
  const WasabiaSong(
      {Key? key,
      required this.value,
      required this.init_change,
      required this.song,
      required this.artist,
      required this.index})
      : super(key: key);
  final int value;
  final int init_change;
  final int index;
  final String song;
  final String artist;

  @override
  _WasabiaSongState createState() => _WasabiaSongState();
}

class _WasabiaSongState extends State<WasabiaSong> {
  int change = 0;
  Color button_color = color_1;

  @override
  initState() {
    change = widget.init_change;
    super.initState();
  }

  Color _return_color(int vote_value) {
    if (change == vote_value) {
      return (vote_value == 1) ? Colors.green : Colors.red;
    } else {
      return color_1;
    }
  }

  Widget VoteButton(String logo, int vote_value) {
    return IconButton(
      splashRadius: 12,
      padding: EdgeInsets.zero,
      constraints: BoxConstraints(),
      onPressed: () {
        setState(() {
          change = (change == vote_value) ? 0 : vote_value;
        });
      },
      icon: SvgPicture.asset(
        "assets/icons/buttons/${logo}.svg",
        semanticsLabel: 'Upvote',
        color: _return_color(vote_value),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      color: Color.fromARGB(0, 0, 0, 0),
      child: Row(mainAxisSize: MainAxisSize.min, children: [
        Padding(
          padding: const EdgeInsets.all(8.0),
          child: Text("${widget.index}"),
        ),
        Padding(
          padding: const EdgeInsets.all(8.0),
          child: new Container(
            height: 42.0,
            width: 42.0,
            color: Color.fromARGB(255, 54, 222, 244),
          ),
        ),
        Padding(
          padding: const EdgeInsets.fromLTRB(8, 0, 8, 0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                widget.song,
                style: TextStyle(
                  fontWeight: FontWeight.bold,
                  fontSize: 16.0,
                ),
              ),
              Text(
                widget.artist,
                style: TextStyle(
                  fontSize: 10.0,
                ),
              ),
            ],
          ),
        ),
        SizedBox(width: 150),
        Column(
          children: <Widget>[
            VoteButton("upvote", 1),
            Text(
              "${widget.value + change}",
              style: TextStyle(
                height: 1,
              ),
            ),
            VoteButton("downvote", -1),
          ],
        ),
      ]),
    );
  }
}
