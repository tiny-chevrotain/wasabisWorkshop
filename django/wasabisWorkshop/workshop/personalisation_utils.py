from .test_utils import get_key, group_input, setup_spotify
from .utils import execute_spotify_api_request, organise_queries
import json

# https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge


def test_spotify_functionality():
    token = setup_spotify()
    playlists_response = execute_spotify_api_request(
        user_auth_token=token,
        endpoint='me/playlists',
        method='GET',
        queries={
            'offset': '0',
            'limit': '20',
        },
    )
    playlist_id = playlists_response['items'][3]['uri'][17:]
    all_songs = get_playlist_songs(playlist_id, token)
    all_songs, all_artists = separate_artists(all_songs)
    all_artist_genres = get_artist_info(all_artists, token)
    all_songs = apply_genres(all_songs, all_artist_genres)

    return {
        'items': all_songs,
        'artists': all_artists,
    }

    # # Opening JSON file
    # f = open('workshop/test_song_properties.json', encoding='cp850')

    # # returns JSON object as
    # # a dictionary
    # all_song_features_dict = json.load(f)


def get_playlist_songs(playlist_id, token):
    count = 0
    finished = False
    all_songs = []
    while (finished == False):
        playlist_response = execute_spotify_api_request(
            user_auth_token=token,
            endpoint=f'playlists/{playlist_id}/tracks',
            method='GET',
            queries={
                'offset': count*100,
                'limit': 100,
                'fields': [
                    'href',
                    'next',
                    'total',
                    {
                        'items': [
                            'is_local',
                            'added_at',
                            {
                                'track': [
                                    'id',
                                    'name',
                                    {
                                        'artists': [
                                            'id',
                                            'name'
                                        ]
                                    },
                                    {
                                        'album': [
                                            'name',
                                            'images',
                                        ]
                                    },
                                ]
                            },
                        ],
                    },
                ],
            },
        )
        count += 1
        all_songs += playlist_response['items']
        if (playlist_response['next'] == None):
            finished = True
    return all_songs


def separate_artists(all_songs):
    '''
        Removes local songs and creates all_artists array
    '''
    online_songs = []
    all_artists = []
    for song in all_songs:
        if not song['is_local']:
            online_songs.append(song)
            for artist in song['track']['artists']:
                same_artists = filter(
                    lambda existing_artist:
                    existing_artist['id'] == artist['id'],
                    all_artists,
                )
                same_artists = list(same_artists)
                if same_artists == []:
                    all_artists.append(artist)
    return online_songs, all_artists


def get_artist_info(all_artists, token):
    all_artists_ids = get_key(all_artists, 'id')
    all_artists_grouped = group_input(all_artists_ids, 50)
    all_artist_genres = []
    for artist_group in all_artists_grouped:
        artists_response = execute_spotify_api_request(
            user_auth_token=token,
            endpoint='artists',
            method='GET',
            queries={'ids': artist_group},
        )
        all_artist_genres += artists_response['artists']
    return all_artist_genres


def apply_genres(all_songs, all_artist_genres):
    for song in all_songs:
        song_artists = get_key(song['track']['artists'], 'id')
        same_artists = filter(
            lambda existing_artist:
            existing_artist['id'] in song_artists,
            all_artist_genres,
        )
        # genre_array_embedded is an array of arrays
        genre_array_embedded = get_key(same_artists, 'genres')

        genre_array = []
        for mini_genre_array in genre_array_embedded:
            genre_array += mini_genre_array  # flattens genre_array_embedded -> genre_array

        genre_array = list(dict.fromkeys(genre_array))  # remove duplicates
        song['genres'] = genre_array
    return all_songs


def get_features(all_songs, token):
    all_features = []
    key_array = []
    for song in all_songs:
        key_array.append(song['track']['id'])

    all_songs_grouped = group_input(key_array, 100)
    for song_group in all_songs_grouped:
        song_features_response = execute_spotify_api_request(
            user_auth_token=token,
            endpoint='audio-features',
            method='GET',
            queries={'ids': song_group},
        )
        all_features += song_features_response['audio_features']

    keys_to_remove = ["type", "uri", "track_href", "analysis_url"]
    for feature in all_features:
        for key in keys_to_remove:
            feature.pop(key)

    for song_count in range(len(all_songs)):
        all_songs[song_count] |= all_features[song_count]

    return all_songs
