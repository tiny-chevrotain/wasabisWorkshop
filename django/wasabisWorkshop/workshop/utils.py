from datetime import timedelta
from django.utils import timezone
from requests import post, put, get

from .credentials import CLIENT_ID, CLIENT_SECRET

from .models import SpotifyToken, User


BASE_URL = "https://api.spotify.com/v1/"

# move this functionality to viewsets:


def get_user_token(session_id):
    tokens = SpotifyToken.objects.filter(session_id=session_id)
    if tokens.exists():
        return tokens[0]
    else:
        return None


def update_or_create_token(session_id, access_token, token_type, expires_in, refresh_token):
    expires_in = timezone.now() + timedelta(seconds=expires_in)
    #user = User.objects.get(id=user_id)
    token = get_user_token(session_id)

    if token:
        token.access_token = access_token
        token.refresh_token = refresh_token
        token.expires_in = expires_in
        token.token_type = token_type
        token.save(update_fields=['access_token',
                   'refresh_token', 'expires_in', 'token_type'])
    else:
        token = SpotifyToken(session_id=session_id, access_token=access_token,
                             refresh_token=refresh_token, token_type=token_type, expires_in=expires_in)
        token.save()


def is_spotify_authenticated(session_id):
    token = get_user_token(session_id)
    if token:
        expiry = token.expires_in
        if expiry <= timezone.now():
            refresh_spotify_token(session_id)
        return True
    return False


def refresh_spotify_token(session_id):
    refresh_token = get_user_token(session_id).refresh_token

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')
    refresh_token = response.get('refresh_token')

    update_or_create_token(
        session_id, access_token, token_type, expires_in, refresh_token)


def execute_spotify_api_request(session_id, endpoint, method='GET', extra_header={}):
    token = get_user_token(session_id)
    print("Successfully recieved")
    print({
        "session_id": session_id,
        "endpoint": endpoint,
        "method": method,
        "token": token.access_token,
        "URL": BASE_URL + endpoint,
    })
    headers = {'Content-Type': 'application/json',
               'Authorization': "Bearer " + token.access_token}
    #headers = headers | extra_header

    match method:
        case 'GET':
            response = get(url=BASE_URL + endpoint, headers=headers)
        case 'POST':
            response = post(BASE_URL + endpoint, headers=headers)
        case 'PUT':
            response = put(BASE_URL + endpoint, headers=headers)

    return response.json()
    # except:
    #     return {'Error': 'Issue with request'}
