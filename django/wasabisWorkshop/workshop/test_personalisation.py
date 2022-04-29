from .personalisation_utils import apply_genres, get_artist_info, get_features, get_playlist_songs, separate_artists
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
            'limit': '50',
        },
    )

    # wasabia_name = 'test_wasabia_2'
    # library_name = "Ollie's music"

    # wasabia = filter(
    #     lambda playlist:
    #     playlist['name'] == wasabia_name,
    #     playlists_response['items'],
    # )
    # library = filter(
    #     lambda playlist:
    #     playlist['name'] == library_name,
    #     playlists_response['items'],
    # )

    # wasabia = generate_playlist_features(
    #     next(wasabia)['uri'][17:], token)
    # user_playlist = generate_playlist_features(
    #     next(library)['uri'][17:], token)

    return playlists_response
    # {
    #     'user_playlist': user_playlist,
    #     'wasabia': wasabia,
    # }


def generate_playlist_features(playlist_id, token):
    all_songs = get_playlist_songs(playlist_id, token)
    all_songs, all_artists = separate_artists(all_songs)
    all_artist_genres = get_artist_info(all_artists, token)
    all_songs = apply_genres(all_songs, all_artist_genres)
    return get_features(all_songs, token)
