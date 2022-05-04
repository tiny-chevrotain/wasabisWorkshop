import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:myapp/api_functions.dart';
import 'package:myapp/create_wasabia_page.dart';
import 'package:myapp/load_page.dart';
import 'package:myapp/global_variables.dart';
import 'package:myapp/wasabia_components.dart';
import 'package:myapp/wasabia_page.dart';
import 'package:image_network/image_network.dart';

//https://codeitoutt.medium.com/how-to-display-anonymous-number-of-images-in-flutter-using-listview-builder-e2e8aaa2fa0a

// final String id;
//   final String name;
//   final String artist;
//   final int votes;
//   final int user_vote;

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
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            Center(
              child: Padding(
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
            ),
            Center(
              child: Padding(
                padding: const EdgeInsets.fromLTRB(0, 8.0, 8.0, 8.0),
                child: ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    primary: color_4,
                  ),
                  child: Text(
                    'Create new wasabia',
                    style: TextStyle(fontSize: 20.0),
                  ),
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) => CreateWasabiaPage(),
                      ),
                    );
                  },
                ),
              ),
            ),
            ListView.builder(
              scrollDirection: Axis.vertical,
              shrinkWrap: true,
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
                                  builder: (context) => LoadWasabiaPage(
                                        id: wasabias[index].id,
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
          ],
        ),
      ),
    );
  }
}

class LoadDiscoverPage extends StatelessWidget {
  const LoadDiscoverPage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return FutureBuilder(
      future: getDiscover('0'),
      builder: (BuildContext context, AsyncSnapshot<List<Wasabia>> snapshot) {
        if (!snapshot.hasData) {
          return LoadingPage();
        } else if (snapshot.data == null) {
          return Scaffold(
            body:
                Text("Ayyo the data is null that aint meant to happen lmaooo."),
          );
        }
        print("This is only happening once, right?");
        return WasabiaListPage(
          wasabias: snapshot.data!,
        );
      },
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
