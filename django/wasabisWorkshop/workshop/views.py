import json
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .personalisation_utils import format_songs, get_all_playlists, get_playlist_songs, get_saved_songs

from .test_utils import format_playlists, format_tracks, get_id_array, get_key, get_songs_with_artists, get_to_make, make_missing_scores, make_missing_songs, split_id_array

from .serializers import DownvoteSerializer, ScoreSerializer, UpvoteSerializer, UserSerializer, WasabiaInfoSerializer, WasabiaSerializer

from .test_personalisation import personalise, test_spotify_functionality

from .models import Artist, Downvote, Score, Song, Upvote, User, Wasabia

from .forms import LoginForm, SignupForm
from .credentials import REDIRECT_URI, CLIENT_ID, CLIENT_SECRET
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from requests import Request, post

from django.contrib import auth

import os
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import random
from django.views.decorators.csrf import csrf_exempt

from .utils import authenticate_user, execute_spotify_api_request, is_spotify_authenticated, update_or_create_token

from rest_framework.decorators import api_view, renderer_classes, authentication_classes, permission_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from django.db.models import Q

# Create your views here.
# https://stackoverflow.com/questions/39647123/salt-in-pbkdf2-python#:~:text=The%20Passlib%20Password%20Hash%20interface%20either%20lets%20you%20set%20the%20salt%20size%2C%20or%20the%20salt%20value%20itself.%20From%20the%20documentation%20on%20pbkdf2_sha256%3A


# https://django-rest-framework-simplejwt.readthedocs.io/en/latest/creating_tokens_manually.html
# https://www.remoteinning.com/blog/how-to-use-jwt-authentication-with-django-rest-framework

@api_view(('POST',))
def signup(request):
    form = SignupForm()
    try:
        if request.method == 'POST':
            form = SignupForm(request.POST)

            if form.is_valid():
                email = form.cleaned_data['email']
                name = form.cleaned_data['name']
                password = form.cleaned_data['password']

                existing_user = User.objects.filter(email=email)

                if not existing_user.exists():

                    # create a new user
                    new_user = User(email=email, name=name, password='')
                    # set user's password
                    new_user.set_password(password)
                    new_user.save()

                    # authenticate user
                    return authenticate_user(email=email, password=password, signup=True)
                else:
                    return Response({'status': 'user_already_exists'}, status=status.HTTP_409_CONFLICT)
            else:
                return Response({'status': 'invalid_form'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': 'invalid_method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    except NameError:
        return Response({'status': 'backend_name_error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(('POST',))
def guest_signup(request):

    form = SignupForm()
    try:
        if request.method == 'POST':
            form = SignupForm(request.POST)
            email = "wasabis_workshop_test_guest@test."
            name = "anonymous"
            password = "random_password"
            new_index = 0
            guest_users = User.objects.filter(
                email__startwith=email)
            if guest_users.exists():
                most_recent_guest = guest_users.latest("date_joined")
                guest_index = int(most_recent_guest.email[32:])
                new_index = guest_index + 1
                print(guest_index)

            email = email + str(new_index)
            existing_user = User.objects.filter(email=email)
            print(existing_user)
            if not existing_user.exists():
                # create a new user
                new_user = User(email=email, name=name, password='')
                # set user's password
                new_user.set_password(password)
                new_user.save()

                # authenticate user
                return authenticate_user(email=email, password=password, signup=True)
            else:
                return Response({'status': 'user_already_exists'}, status=status.HTTP_409_CONFLICT)
        else:
            return Response({'status': 'invalid_method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    except NameError:
        return Response({'status': 'backend_name_error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(('POST',))
def login(request):
    form = LoginForm()
    try:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                return authenticate_user(email=email, password=password)
            else:
                # invalid form
                return Response({'status': 'invalid_form'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': 'invalid_method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    except NameError:
        return Response({'status': 'backend_name_error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(('POST',))
@authentication_classes((TokenAuthentication,))
def token_login(request):
    return Response({'status': 'logged_in'}, status=status.HTTP_200_OK)


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class SpotifyTest(APIView):
    def get(self, request, format=None):
        response = execute_spotify_api_request(
            session_id=self.request.session.session_key,
            endpoint="playlists/1aGCxSHK4noZhGVa961sD2/tracks")
        return Response(
            data=response)


@api_view(('POST',))
@authentication_classes((TokenAuthentication,))
def spotify_create_token(request):
    user_token = request.headers['Authorization'][6:]
    spotify_code = request.POST['code']

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': spotify_code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')

    print({
        "access_token": access_token,
        "token_type": token_type,
        "refresh_token": refresh_token,
        "expires_in": expires_in,
        "error": error,
    })

    if not request.session.exists(request.session.session_key):
        request.session.create()

    update_or_create_token(
        user_token, access_token, token_type, expires_in, refresh_token)

    return Response({'status': 'spotify_athenticated'}, status=status.HTTP_200_OK)


class IsAuthenticated(APIView):
    def get(self, request, format=None):
        is_authenticated = is_spotify_authenticated(
            self.request.session.session_key)
        return Response({'status': is_authenticated}, status=status.HTTP_200_OK)


@api_view(('GET',))
@ authentication_classes((TokenAuthentication,))
def get_recommendations(request):
    user_token = request.headers['Authorization'][6:]
    body = request.GET
    wasabia_id = int(body['wasabia_id'])
    wasabia = Wasabia.objects.get(id=wasabia_id)
    recommendations = personalise(wasabia, user_token)
    print(recommendations)
    return Response({'recommendations': recommendations}, status=status.HTTP_200_OK)


@api_view(('GET',))
@authentication_classes((TokenAuthentication,))
def get_wasabia_list(request):
    all_wasabias = Wasabia.objects.all()
    all_wasabias_serialized = WasabiaInfoSerializer(all_wasabias, many=True)
    all_wasabias_data = all_wasabias_serialized.data
    print(all_wasabias_data)
    all_wasabias_data = sorted(
        all_wasabias_data, key=lambda d:
        d['votes']['votes_total__sum'] if d['votes']['votes_total__sum'] != None else 0, reverse=True)
    return Response({'wasabias': all_wasabias_data}, status=status.HTTP_200_OK)


@ api_view(('POST',))
@ authentication_classes((TokenAuthentication,))
def create_wasabia(request):
    body = request.POST
    user_token = request.headers['Authorization'][6:]
    user = Token.objects.get(key=user_token).user
    wasabia = Wasabia.objects.create(user_id=user.id,
                                     name=body['name'], description=body['description'])
    wasabia.save()
    wasabia_serialized = WasabiaSerializer(wasabia)
    return Response({'wasabia': wasabia_serialized.data}, status=status.HTTP_200_OK)


@ api_view(('GET',))
@ authentication_classes((TokenAuthentication,))
def get_wasabia(request):
    body = request.GET
    user_token = request.headers['Authorization'][6:]
    user = Token.objects.get(key=user_token).user
    wasabia_id = body.get('id', '')
    wasabia = Wasabia.objects.get(id=wasabia_id)
    user_upvotes = Upvote.objects.filter(
        Q(user=user) & Q(score__wasabia=wasabia))
    user_downvotes = Downvote.objects.filter(
        Q(user=user) & Q(score__wasabia=wasabia))
    wasabia_serialized = WasabiaSerializer(wasabia)
    user_upvotes_serialized = UpvoteSerializer(user_upvotes, many=True)
    user_downvotes_serialized = DownvoteSerializer(user_downvotes, many=True)
    wasabia_dict = json.loads(json.dumps(wasabia_serialized.data))
    wasabia_dict['scores'] = sorted(
        wasabia_dict['scores'], key=lambda d: int(d['votes_total']), reverse=True)
    return Response(
        {
            'wasabia': wasabia_dict,
            'upvotes': user_upvotes_serialized.data,
            'downvotes': user_downvotes_serialized.data,
        },
        status=status.HTTP_200_OK,
    )


@ api_view(('PUT',))
@ authentication_classes((TokenAuthentication,))
def add_songs(request):
    body = json.loads(request.body)
    songs_dict = body['songs']
    wasabia_id = body['wasabia_id']
    user_token = request.headers['Authorization'][6:]
    user = Token.objects.get(key=user_token).user

    song_ids = get_key(songs_dict, 'id')
    wasabia = Wasabia.objects.get(id=wasabia_id)

    # is song in database?
    existing_songs = Song.objects.filter(id__in=song_ids)
    existing_song_ids, remaining_song_ids, existing_songs = split_id_array(
        song_ids, [], existing_songs)
    if remaining_song_ids != []:  # if yes
        # do artist loop
        songs_to_make = get_songs_with_artists(
            remaining_song_ids, song_ids, songs_dict)
        # make missing songs & add to existing songs:
        existing_songs += make_missing_songs(songs_to_make)

    # is song in score?
    existing_scores = Score.objects.filter(
        Q(song__in=existing_songs), Q(wasabia__id=wasabia.id))
    existing_song_ids, remaining_song_ids, existing_scores = split_id_array(
        existing_song_ids, remaining_song_ids, existing_scores, id='song__id')
    if remaining_song_ids != []:  # if yes
        # filter in existing songs for remaining ids
        songs_of_scores_to_make = get_to_make(
            remaining_song_ids, song_ids, existing_songs)
        # add to existing scores
        existing_scores += make_missing_scores(
            songs_of_scores_to_make, wasabia)
    for score in existing_scores:
        score.upvote(user)
    return Response({'status': 'added'}, status=status.HTTP_200_OK)


@api_view(('GET',))
@authentication_classes((TokenAuthentication,))
def search_spotify(request):
    body = request.GET
    search = body.get('search', '')
    songs = []
    if search != '':
        user_token = request.headers['Authorization'][6:]
        if is_spotify_authenticated(user_token):
            playlist_response = execute_spotify_api_request(
                user_auth_token=user_token,
                endpoint=f'search',
                method='GET',
                queries={
                    'limit': 50,
                    'q': search,
                    'type': 'track',
                },
            )
            songs = format_tracks(playlist_response['tracks']['items'])
        else:
            # catch that?
            pass
    else:
        # catch this too..
        pass
    return Response({'songs': songs}, status=status.HTTP_200_OK)


@api_view(('GET',))
@authentication_classes((TokenAuthentication,))
def get_playlists(request):
    playlists_formatted = []
    user_token = request.headers['Authorization'][6:]
    if is_spotify_authenticated(user_token):
        playlists = get_all_playlists(user_token)
        playlists_formatted = format_playlists(playlists)
    else:
        # catch that?
        pass
    return Response({'playlists': playlists_formatted}, status=status.HTTP_200_OK)


@api_view(('GET',))
@authentication_classes((TokenAuthentication,))
def get_user_library(request):
    body = request.GET
    existing_playlist_ids = body.get('playlist_ids', '')
    saved = body.get('saved', '')
    existing_playlist_ids = [
        int(id) for id in existing_playlist_ids.split(',')
    ]
    playlists = []
    saved_songs = []
    user_token = request.headers['Authorization'][6:]
    if is_spotify_authenticated(user_token):
        playlists = get_all_playlists(user_token)
        playlist_ids = get_key(playlists, 'id')
        playlist_ids = [
            id for id in playlist_ids if id not in existing_playlist_ids
        ]
        for playlist_count in range(len(playlist_ids)-1):
            playlist_songs = get_playlist_songs(
                playlist_ids[playlist_count], user_token)
            playlists['tracks'] = format_songs(playlist_songs)
        if saved == '':
            saved_songs = get_saved_songs(user_token)
            saved_songs = format_songs(saved_songs)
    else:
        # catch that
        pass
    return Response({'playlists': playlists, 'saved_songs': saved_songs}, status=status.HTTP_200_OK)


@api_view(('GET',))
@authentication_classes((TokenAuthentication,))
def get_user_saved_songs(request):
    saved_songs = []
    user_token = request.headers['Authorization'][6:]
    if is_spotify_authenticated(user_token):
        saved_songs = get_saved_songs(user_token)
        saved_songs = format_songs(saved_songs)
    else:
        # catch that
        print("error")
        pass
    return Response({'saved_songs': saved_songs}, status=status.HTTP_200_OK)


@api_view(('GET',))
@authentication_classes((TokenAuthentication,))
def get_user_playlist_songs(request):
    user_token = request.headers['Authorization'][6:]
    body = request.GET
    playlist_id = body.get('id')
    playlist_songs = []
    if playlist_id:
        if is_spotify_authenticated(user_token):
            playlist_songs = get_playlist_songs(
                playlist_id, user_token)
            playlist_songs = format_songs(playlist_songs)
        else:
            # catch that
            pass
    else:
        # catch that
        pass
    return Response({'playlist_songs': playlist_songs}, status=status.HTTP_200_OK)


@api_view(('PUT',))
@authentication_classes((TokenAuthentication,))
def song_vote(request):
    user_token = request.headers['Authorization'][6:]
    user = Token.objects.get(key=user_token).user
    body = request.POST
    vote = int(body['vote'])
    song_id = body['song_id']
    wasabia_id = int(body['wasabia_id'])
    score = Score.objects.get(Q(wasabia__id=wasabia_id) & Q(song__id=song_id))
    score.vote(user, vote)
    score_serialized = ScoreSerializer(score)
    return Response({'status': 'successfully voted', 'score': score_serialized.data}, status=status.HTTP_200_OK)
