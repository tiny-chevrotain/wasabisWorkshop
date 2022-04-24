from datetime import timedelta
from django.utils import timezone
from requests import post, put, get

from .credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

from .models import SpotifyToken, User

from rest_framework.authtoken.models import Token

from .models import User
from rest_framework import status
from rest_framework.response import Response

from django.contrib import auth

from requests import Request


BASE_URL = "https://api.spotify.com/v1/"


def get_token(user_auth_token):
    tokens = SpotifyToken.objects.filter(user_auth_token=user_auth_token)
    if tokens.exists():
        return tokens[0]
    else:
        return None


def update_or_create_token(user_auth_token, access_token, token_type, expires_in, refresh_token):
    expires_in = timezone.now() + timedelta(seconds=expires_in)
    token = get_token(user_auth_token)

    if token:
        token.access_token = access_token
        token.refresh_token = refresh_token
        token.expires_in = expires_in
        token.token_type = token_type
        token.save(update_fields=['access_token',
                   'refresh_token', 'expires_in', 'token_type'])
    else:
        token = SpotifyToken(user_auth_token=user_auth_token, access_token=access_token,
                             refresh_token=refresh_token, token_type=token_type, expires_in=expires_in)
        token.save()


def is_spotify_authenticated(user_auth_token):
    token = get_token(user_auth_token)
    if token:
        expiry = token.expires_in
        if expiry <= timezone.now():
            refresh_spotify_token(user_auth_token)
        return True
    return False


def refresh_spotify_token(user_auth_token):
    refresh_token = get_token(user_auth_token).refresh_token

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
        user_auth_token, access_token, token_type, expires_in, refresh_token)


def execute_spotify_api_request(user_auth_token, endpoint, method='GET', extra_header={}):
    token = get_token(user_auth_token)
    print("Successfully recieved")
    print({
        "user_auth_token": user_auth_token,
        "endpoint": endpoint,
        "method": method,
        "token": token.access_token,
        "URL": BASE_URL + endpoint,
    })
    headers = {'Content-Type': 'application/json',
               'Authorization': "Bearer " + token.access_token}
    headers = headers | extra_header

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


def authenticate_user(email="", password="", signup=False):
    user = auth.authenticate(email=email, password=password)
    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        body = {
            'status': 'logged_in',
            'token': token.key,
            'spotify_auth': 'true',
        }
        if not is_spotify_authenticated(token):
            url = get_auth_url()
            body['url'] = url
            body['spotify_auth'] = 'false'
        return Response(body, status=status.HTTP_200_OK)
    elif signup:
        # this should never happen
        return Response({'status': 'user_somehow_none??'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        # failed authentication
        return Response({'status': 'invalid_credentials'}, status=status.HTTP_401_UNAUTHORIZED)


def get_auth_url():
    print("We are authorising, nothing fancy and no tokens set")
    scopes = 'user-library-modify user-library-read app-remote-control playlist-modify-public'
    return Request('GET', 'https://accounts.spotify.com/authorize', params={
        'scope': scopes,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
    }).prepare().url
