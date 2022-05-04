from .models import Artist, Score, Song
from .utils import is_spotify_authenticated


def setup_spotify():
    user_token = "7f3a8cfe4d5e9d2a5e456224f3f1f8b187c72c44"
    print(is_spotify_authenticated(user_token))  # will refresh
    return user_token


def group_input(input_array, grouping):
    def grouped(iterable, n):
        return zip(*[iter(iterable)]*n)

    groups = grouped(input_array, grouping)
    group_array = []

    for item in groups:
        group_array.append(item)

    final_group = input_array[len(group_array)*grouping:]

    group_array.append(final_group)

    return group_array


def get_key(dict_array, key):
    key_array = []
    for dict in dict_array:
        key_array.append(dict[key])
    return key_array


def get_id_array(model_objects, id='id'):
    return get_key(list(model_objects.values(id)), id)


def split_id_array(original_ids, remaining_ids, model_objects, id='id'):
    if model_objects.exists():
        _existing_ids = get_id_array(model_objects, id=id)
        _remaining_ids = [
            id for id in original_ids if id not in _existing_ids]
        return _existing_ids, remaining_ids+_remaining_ids, list(model_objects)
    else:
        return [], remaining_ids+original_ids, []


def get_to_make(remaining_ids, original_ids, dict_array):
    to_make = []
    for id in remaining_ids:
        index = original_ids.index(id)
        to_make.append(dict_array[index])
    return to_make


def get_songs_with_artists(remaining_song_ids, song_ids, songs_dict):
    songs_to_make = get_to_make(remaining_song_ids, song_ids, songs_dict)
    for song in songs_to_make:
        artist_ids = get_key(song['artists'], 'id')
        existing_artists = Artist.objects.filter(id__in=artist_ids)
        _, remaining_artist_ids, existing_artists = split_id_array(
            artist_ids, [], existing_artists)
        if artist_ids != []:
            artists_to_make = get_to_make(
                remaining_artist_ids, artist_ids, song['artists'])
            artist_objects = Artist.objects.bulk_create(
                [
                    Artist(
                        id=artist['id'],
                        name=artist['name'],
                    )
                    for artist in artists_to_make
                ]
            )
            existing_artists += artist_objects
        song['artist_objects'] = existing_artists
    return songs_to_make


def make_missing_songs(songs_to_make):
    song_objects = Song.objects.bulk_create(
        [
            Song(
                id=song['id'],
                name=song['name'],
                image_640_url=song['image_640_url'],
                image_300_url=song['image_300_url'],
                image_64_url=song['image_64_url'],
            )
            for song in songs_to_make
        ]
    )
    for song_count in range(len(songs_to_make)):
        # ------- do all this to reduce number of hits to database!
        song_objects[song_count].artists.set(
            songs_to_make[song_count]['artist_objects'])
        song_objects[song_count].save()
    return song_objects


def make_missing_scores(songs_of_scores_to_make, wasabia):
    # add to wasabia
    wasabia.songs.add(*songs_of_scores_to_make)
    # create scores
    return Score.objects.bulk_create(
        [
            Score(
                song=song,
                wasabia=wasabia,
            )
            for song in songs_of_scores_to_make
        ]
    )


def format_songs(unformatted_songs):
    formatted_songs = []
    for song in unformatted_songs:
        if not song['is_local']:
            formatted_song = {
                'id': song['track']['id'],
                'name': song['track']['name'],
                "artists": song['track']['artists'],
            }
            if (len(song['track']['album']['images']) == 3):
                formatted_song |= {
                    'image_640_url': song['track']['album']['images'][0]['url'],
                    'image_300_url': song['track']['album']['images'][1]['url'],
                    'image_64_url': song['track']['album']['images'][2]['url'],
                }
            formatted_songs.append(formatted_song)
    return formatted_songs


def format_tracks(unformatted_tracks):
    formatted_tracks = []
    for song in unformatted_tracks:
        formatted_track = {
            'id': song['id'],
            'name': song['name'],
            "artists": song['artists'],
        }
        if (len(song['album']['images']) == 3):
            formatted_track |= {
                'image_640_url': song['album']['images'][0]['url'],
                'image_300_url': song['album']['images'][1]['url'],
                'image_64_url': song['album']['images'][2]['url'],
            }
        formatted_tracks.append(formatted_track)
    return formatted_tracks


def format_playlists(unformatted_playlists):
    formatted_playlists = []
    for playlist in unformatted_playlists:
        formatted_track = {
            'id': playlist['id'],
            'image_url': playlist['images'][0]['url'],
            "name": playlist['name'],
            'total': playlist['tracks']['total'],
            'tracks': [],
        }
        formatted_playlists.append(formatted_track)
    return formatted_playlists
