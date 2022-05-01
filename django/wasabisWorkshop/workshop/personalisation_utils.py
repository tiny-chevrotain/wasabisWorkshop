import datetime
from .test_utils import get_id_array, get_key, group_input, setup_spotify
from .utils import execute_spotify_api_request
import json
from collections import Counter
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
pd.options.mode.chained_assignment = None
# gets rid of annoying false-positive warning

# https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge

# ----------- for debugging only:


def get_wasabia_ids_debug(playlist_id, token):
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
                    'next',
                    {
                        'items': [
                            'is_local',
                            {
                                'track': [
                                    'id',
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
    song_ids = []
    for song in all_songs:
        song_ids.append(song['track']['id'])
    return song_ids

# ----------- grab data:


def get_wasabia_song_ids(wasabia):
    songs = wasabia.songs.all()
    song_ids = songs.values('id')
    return get_id_array(song_ids, id='id')


def format_tracks(bad_format_tracks):
    current_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    return [
        {
            'is_local': False,
            'added_at': current_time,
            'track': {
                'id': bad_track['id'],
                'name': bad_track['name'],
                'artists': [
                    {
                        'id': artist['id'],
                        'name': artist['name'],
                    }
                    for artist in bad_track['artists']
                ],
                'album': {
                    'name': bad_track['album']['name'],
                    'images': bad_track['album']['images'],
                    'release_date': bad_track['album']['release_date'],
                },
            }
        }
        for bad_track in bad_format_tracks
    ]


def get_tracks(track_ids, token):
    all_tracks = []
    all_ids_grouped = group_input(track_ids, 50)
    for id_group in all_ids_grouped:
        playlist_response = execute_spotify_api_request(
            user_auth_token=token,
            endpoint=f'tracks',
            method='GET',
            queries={
                'ids': id_group
            }
        )
        all_tracks += playlist_response['tracks']
    return format_tracks(all_tracks)


def get_all_playlists(token):
    count = 0
    finished = False
    all_playlists = []
    while (finished == False):
        playlists_response = execute_spotify_api_request(
            user_auth_token=token,
            endpoint='me/playlists',
            method='GET',
            queries={
                'offset': count*50,
                'limit': '50',
            },
        )
        count += 1
        all_playlists += playlists_response['items']
        if (playlists_response['next'] == None):
            finished = True
    return all_playlists


def get_all_playlist_ids(token):
    all_playlists = get_all_playlists(token)
    playlist_ids = []
    for playlist in all_playlists:
        playlist_ids.append(playlist['uri'][17:])
    return playlist_ids


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
                                            'release_date',
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


def format_songs(bad_format_songs):
    return [
        {
            'is_local': False,
            'added_at': bad_song['added_at'],
            'track': {
                'id': bad_song['track']['id'],
                'name': bad_song['track']['name'],
                'artists': [
                    {
                        'id': artist['id'],
                        'name': artist['name'],
                    }
                    for artist in bad_song['track']['artists']
                ],
                'album': {
                    'name': bad_song['track']['album']['name'],
                    'images': bad_song['track']['album']['images'],
                    'release_date': bad_song['track']['album']['release_date'],
                },
            }
        }
        for bad_song in bad_format_songs
    ]


def get_saved_songs(token):
    count = 0
    finished = False
    all_songs = []
    while (finished == False):
        song_response = execute_spotify_api_request(
            user_auth_token=token,
            endpoint='me/tracks',
            method='GET',
            queries={
                'offset': count*50,
                'limit': '50',
            },
        )
        count += 1
        all_songs += format_songs(song_response['items'])
        if (song_response['next'] == None):
            finished = True
    return all_songs


def get_library_songs(token):
    playlist_ids = get_all_playlist_ids(token)
    all_songs = []
    for playlist_id in playlist_ids:
        all_songs += get_playlist_songs(playlist_id, token)
    all_songs += get_saved_songs(token)
    return all_songs


def remove_duplicate_songs(all_songs):
    unique_song_ids = []
    unique_songs = []
    for song in all_songs:
        current_id = song['track']['id']
        if current_id not in unique_song_ids:
            unique_song_ids.append(current_id)
            unique_songs.append(song)
    return unique_songs


def remove_local_songs(all_songs):
    online_songs = []
    for song in all_songs:
        if not song['is_local']:
            online_songs.append(song)
    return online_songs


def separate_artists(all_songs):
    '''
        Removes local songs and creates all_artists array
    '''
    all_artists = []
    for song in all_songs:
        for artist in song['track']['artists']:
            same_artists = filter(
                lambda existing_artist:
                existing_artist['id'] == artist['id'],
                all_artists,
            )
            same_artists = list(same_artists)
            if same_artists == []:
                all_artists.append(artist)
    return all_artists


def get_artist_info(all_artists, token):
    all_artists_ids = get_key(all_artists, 'id')
    all_artists_grouped = group_input(all_artists_ids, 50)
    all_artist_genres = []
    for artist_group in all_artists_grouped:
        if artist_group != []:
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
        all_songs[song_count]['release_date'] = all_songs[song_count]['track']['album']['release_date']
        # debug line \/\/
        all_songs[song_count]['name'] = all_songs[song_count]['track']['name']
        # debug line^^
        all_songs[song_count] |= all_features[song_count]

    return all_songs

# ---------- pandas calculations:


def generate_dataframes(library_songs, wasabia_songs):

    library_songs_df = pd.DataFrame(library_songs)
    wasabia_songs_df = pd.DataFrame(wasabia_songs)

    library_songs_df = library_songs_df.drop_duplicates(subset=['id'])
    wasabia_songs_df = wasabia_songs_df.drop_duplicates(subset=['id'])

    library_songs_length = len(library_songs_df.index)
    wasabia_songs_length = len(wasabia_songs_df.index)

    return library_songs_df, wasabia_songs_df, library_songs_length, wasabia_songs_length


def generate_all_dataframe(library_songs_df, wasabia_songs_df):
    all_songs_df = pd.concat(
        [library_songs_df, wasabia_songs_df]).reset_index(drop=True)
    all_songs_df['year'] = all_songs_df['release_date'].apply(
        lambda x: x.split('-')[0])
    return all_songs_df.drop(['release_date', 'is_local', 'track'], axis=1)


def collate_genre_stats(all_songs_df):
    genre_weights_df = pd.read_csv(
        'workshop/data/genre_weights.csv', index_col=0)
    # grabbin it again bc we need to use it. this code can be re-used lol
    float_cols = all_songs_df.dtypes[all_songs_df.dtypes ==
                                     'float64'].index.values
    int_cols = all_songs_df.dtypes[all_songs_df.dtypes == 'int64'].index.values
    return np.concatenate((float_cols, int_cols), axis=None), genre_weights_df


def ohe_prep(df, column):
    """ 
    Create One Hot Encoded features of a specific column

    Parameters: 
        df (pandas dataframe): Spotify Dataframe
        column (str): Column to be processed

    Returns: 
        tf_df: One hot encoded features 
    """

    tf_df = pd.get_dummies(df[column])
    tf_df.reset_index(drop=True, inplace=True)
    return tf_df


def create_feature_set(df, stat_cols, genre_weights_df):
    """ 
    Process spotify df to create a final set of features that will be used to generate recommendations

    Parameters: 
        df (pandas dataframe): Spotify Dataframe
        stat_cols (list(str)): List of float columns that will be scaled 

    Returns: 
        final: final set of features 
    """
    song_genre_weights_df = (
        df['genres'].explode()
        .str.get_dummies().sum(level=0)
    )

    for genre in song_genre_weights_df.columns.values:
        song_genre_weights_df[genre] *= genre_weights_df.loc[genre].values[0]

    year_ohe = ohe_prep(df, 'year') * 0.5

    # scale float columns
    floats = df[stat_cols].reset_index(drop=True)
    scaler = MinMaxScaler()
    floats_scaled = pd.DataFrame(scaler.fit_transform(
        floats), columns=floats.columns) * 0.2

    # concanenate all features
    final = pd.concat([song_genre_weights_df, floats_scaled, year_ohe,
                      df['added_at']], axis=1).sort_values('added_at', ascending=False)
    # final = pd.concat([song_genre_weights_df, floats_scaled, df['added_at']], axis = 1).sort_values('added_at',ascending = False)

    final['id'] = df['id'].values

    return final.reset_index(drop=True).copy()


def summarise_playlist(playlist_df, weight_decay, not_playlist=False):
    """
    Summarize a user's playlist into a single vector

    Parameters: 
        playlist_df (pandas dataframe): playlist dataframe
        weight_factor (float): float value that represents the recency bias. The larger the recency bias, the most priority recent songs get. Value should be close to 1. 

    Returns: 
        playlist_feature_set_weighted_final (pandas series): single feature that summarizes the playlist
        complete_feature_set_nonplaylist (pandas dataframe): 
    """
    if not_playlist:
        return playlist_df.sum(axis=0).drop('id')
    else:
        playlist_feature_set = playlist_df.sort_values(
            'added_at', ascending=False)
        most_recent_date = playlist_feature_set['added_at'][0]
        for ix, row in playlist_feature_set.iterrows():
            playlist_feature_set.loc[ix, 'months_from_recent'] = int(
                (pd.to_datetime(most_recent_date) - pd.to_datetime(row['added_at'])).days / 30)
        playlist_feature_set['weight'] = playlist_feature_set['months_from_recent'].apply(
            lambda x: weight_decay ** (-x))
        playlist_feature_set_weighted = playlist_feature_set.copy()
        playlist_feature_set_weighted.update(
            playlist_feature_set_weighted.iloc[:, :-4].mul(playlist_feature_set_weighted.weight, 0))
        playlist_feature_set_weighted_final = playlist_feature_set_weighted.iloc[:, :-4]
    return playlist_feature_set_weighted_final.mean(axis=0)


def find_cosine_similarity(playlist_summary, wasabia_features):
    """ 
    Pull songs from a specific playlist.

    Parameters: 
        playlist_summary (pandas series): summarized playlist feature
        wasabia_features (pandas dataframe): feature set of songs that are not in the selected playlist

    Returns: 
        non_playlist_df_top_40: Top 40 recommendations for that playlist
    """

    wasabia_df = wasabia_features[['id']]
    wasabia_df['sim'] = cosine_similarity(wasabia_features.drop(
        'id', axis=1).values, playlist_summary.values.reshape(1, -1))[:, 0]
    wasabia_df = wasabia_df.sort_values('sim', ascending=False)

    return wasabia_df


def find_similarity(feature_set, library_songs_length, wasabia_songs_length, wasabia_songs_df):
    library_features_df = feature_set.head(library_songs_length)
    wasabia_features_df = feature_set.tail(
        wasabia_songs_length).drop(['added_at'], axis=1)

    summarised_library_features = summarise_playlist(library_features_df, 1.09)

    wasabia_cosine_similarity = find_cosine_similarity(
        summarised_library_features, wasabia_features_df)

    wasabia_songs_df = wasabia_songs_df.set_index('id')

    wasabia_songs_df['sim'] = wasabia_cosine_similarity.set_index('id')['sim']

    return wasabia_songs_df.sort_values('sim', ascending=False)

# find_similarity(feature_set, library_songs_length, wasabia_songs_length, wasabia_songs_df)
