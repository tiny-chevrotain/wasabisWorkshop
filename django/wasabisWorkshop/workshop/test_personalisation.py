from .test_utils import setup_spotify
from .utils import execute_spotify_api_request, organise_queries


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
    playlist_id = playlists_response['items'][0]['uri'][17:]
    count = 0
    finished = False
    all_songs_dict = {
        'items': []
    }
    while (count < 30 or finished == False):
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
                            {
                                'track': [
                                    'id',
                                    'name',
                                    {
                                        'artists': 'name'
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
        print(count)
        all_songs_dict['items'] += playlist_response['items']
        if (playlist_response['next'] == None):
            finished = True
    return all_songs_dict
    # print("Got here?")
