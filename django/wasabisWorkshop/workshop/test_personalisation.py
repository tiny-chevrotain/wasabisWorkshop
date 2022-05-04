from .personalisation_utils import apply_genres, collate_genre_stats, create_feature_set, find_similarity, generate_all_dataframe, generate_dataframes, get_artist_info, get_features, get_library_songs, get_tracks, get_wasabia_song_ids, remove_duplicate_songs, remove_local_songs, separate_artists
from .test_utils import setup_spotify
import pandas as pd
pd.options.mode.chained_assignment = None

# https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge

# https://www.youtube.com/watch?v=BbPswIqn2VI <- for future development, consider progress bar w/ celery


def test_spotify_functionality():
    token = setup_spotify()
    # id is for debug, remove to gather from database in future:
    return personalise('1tSDFBwuUGqGhw61KuYETZ', token)


def personalise(wasabia, token):
    print("Getting library")
    user_library = get_library_songs(token)
    print("Removing duplicates")
    user_library = remove_duplicate_songs(user_library)
    print("Removing local songs")
    user_library = remove_local_songs(user_library)

    print("Getting wasabia ids")
    wasabia_song_ids = get_wasabia_song_ids(wasabia)
    print(wasabia_song_ids)
    print("Getting wasabia tracks")
    wasabia = get_tracks(wasabia_song_ids, token)

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

    song_ids = list(suggestions_dict['track'].keys())
    songs_formatted = []
    for id in song_ids:
        current_track = suggestions_dict['track'][id]
        current_track['sim'] = suggestions_dict['sim'][id]
        songs_formatted.append(current_track)
    return songs_formatted
