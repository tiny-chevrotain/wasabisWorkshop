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

# # Opening JSON file
# f = open('workshop/test_song_properties.json', encoding='cp850')

# # returns JSON object as
# # a dictionary
# all_song_features_dict = json.load(f)

# import pandas as pd
# import numpy as np
# import json
# import re
# import sys
# import itertools

# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# from sklearn.preprocessing import MinMaxScaler
# import matplotlib.pyplot as plt

# import sqlite3

# import warnings
# # warnings.filterwarnings("ignore")


# # pd.set_option('display.max_columns', None)
# # pd.set_option("max_rows", None)
# # maybe re-introduce this... idk what it does lol 💀


# try:
#     conn = sqlite3.connect("million_songs.db")
# except Exception as e:
#     print(e)

# # Now in order to read in pandas dataframe we need to know table name
# cursor = conn.cursor()
# songs_df = pd.read_sql_query('SELECT * FROM FEATURES_2', conn)
# many_genres_df = pd.read_sql_query('SELECT * FROM TRAINING_DB_2', conn)
# conn.close()

# print(songs_df.head())
# print(many_genres_df.head())
