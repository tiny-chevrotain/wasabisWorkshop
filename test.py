# import json

# with open('./personalise_test.json') as json_file:
#     test_data_json = json.load(json_file)

# formatted_tracks = []
# for song in test_data_json['user_playlist']:
#     if (len(song['track']['album']['images']) == 3):
#         formatted_tracks.append(
#             {
#                 'id': song['id'],
#                 'name': song['name'],
#                 "artists": song['track']['artists'],
#                 'image_640_url': song['track']['album']['images'][0]['url'],
#                 'image_300_url': song['track']['album']['images'][1]['url'],
#                 'image_64_url': song['track']['album']['images'][2]['url'],
#             }
#         )

# with open('formatted_songs.json', 'w') as f:
#     json.dump({'songs': formatted_tracks}, f)

array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2]

print(array.index(2))
