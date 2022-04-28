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
            'limit': '20',
        },
    )

    user_playlist = generate_playlist_features(
        playlists_response['items'][0]['uri'][17:], token)
    wasabia = generate_playlist_features(
        playlists_response['items'][1]['uri'][17:], token)

    return {
        'user_playlist': user_playlist,
        'wasabia': wasabia,
    }


def generate_playlist_features(playlist_id, token):
    all_songs = get_playlist_songs(playlist_id, token)
    all_songs, all_artists = separate_artists(all_songs)
    all_artist_genres = get_artist_info(all_artists, token)
    all_songs = apply_genres(all_songs, all_artist_genres)
    return get_features(all_songs, token)
