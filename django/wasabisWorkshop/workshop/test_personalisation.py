from .personalisation_utils import apply_genres, collate_genre_stats, create_feature_set, find_similarity, generate_all_dataframe, generate_dataframes, get_artist_info, get_features, get_library_songs, get_playlist_songs, get_saved_songs, get_tracks, get_wasabia_ids, remove_duplicate_songs, remove_local_songs, separate_artists
from .test_utils import get_key, group_input, setup_spotify
from .utils import execute_spotify_api_request, organise_queries
import json
import pandas as pd
import numpy as np
import os
pd.options.mode.chained_assignment = None

# https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge


def test_spotify_functionality():
    token = setup_spotify()
    # id is for debug, remove to gather from database in future:
    return generate_playlist_features('1tSDFBwuUGqGhw61KuYETZ', token)


def generate_playlist_features(playlist_id, token):
    print("Getting library")
    user_library = get_library_songs(token)
    print("Removing duplicates")
    user_library = remove_duplicate_songs(user_library)
    print("Removing local songs")
    user_library = remove_local_songs(user_library)

    # later get this from database:
    print("Getting wasabia ids")
    wasabia_ids = get_wasabia_ids(playlist_id, token)
    print("Getting wasabia tracks")
    wasabia = get_tracks(wasabia_ids, token)
    print("Removing duplicates")
    wasabia = remove_duplicate_songs(wasabia)

    cuttoff_point = len(user_library)
    all_songs = user_library + wasabia  # do this to make less requests for artists

    print("Separating artists")
    all_artists = separate_artists(all_songs)
    print("Getting artist info")
    all_artist_genres = get_artist_info(all_artists, token)
    print("Applying genres")
    all_songs = apply_genres(all_songs, all_artist_genres)
    print("Getting features")
    all_songs = get_features(all_songs, token)

    user_library = all_songs[:cuttoff_point]
    wasabia = all_songs[cuttoff_point:]

    print("Generating data")
    library_df, wasabia_df, library_length, wasabia_length = generate_dataframes(
        user_library, wasabia)
    all_songs_df = generate_all_dataframe(library_df, wasabia_df)
    stat_cols, genre_weights_df = collate_genre_stats(all_songs_df)
    print("Finding similarities")
    feature_set = create_feature_set(all_songs_df, stat_cols, genre_weights_df)
    wasabia_df = find_similarity(
        feature_set, library_length, wasabia_length, wasabia_df)
    print("Converting to output")
    suggestions_dict = wasabia_df.drop(['added_at', 'is_local', 'release_date', 'danceability', 'energy', 'key', 'loudness', 'mode',
                                       'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature'], axis=1).to_dict()

    return suggestions_dict
