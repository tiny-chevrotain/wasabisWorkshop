from .test_utils import setup_spotify
from .utils import execute_spotify_api_request, organise_queries


def test_spotify_functionality():
    token = setup_spotify()
    # playlists_response = execute_spotify_api_request(
    #     user_auth_token=token,
    #     endpoint='me/playlists',
    #     method='GET',
    #     queries={
    #         'offset': '0',
    #         'limit': '20',
    #     },
    # )
    # playlist_id = playlists_response['items'][0]['uri'][17:]
    playlist_id = '1aGCxSHK4noZhGVa961sD2'
    return execute_spotify_api_request(
        user_auth_token=token,
        endpoint=f'playlists/{playlist_id}/tracks',
        method='GET',
        queries={
            'fields': [
                'total',
            ],
        },
    )
    # print("Got here?")
    # print(organise_queries(
    #     {
    #         'offset': '0',
    #         'fields': [
    #             # 'href',
    #             # 'next',
    #             'total',
    #             # {
    #             #     'items': [
    #             #         'is_local',
    #             #         {
    #             #             'track': [
    #             #                 'id',
    #             #                 'name',
    #             #                 {
    #             #                     'artists': 'name'
    #             #                 },
    #             #                 {
    #             #                     'album': [
    #             #                         'name',
    #             #                         'images',
    #             #                     ]
    #             #                 },
    #             #             ]
    #             #         },
    #             #     ],
    #             # },
    #         ],
    #     }
    # ))
