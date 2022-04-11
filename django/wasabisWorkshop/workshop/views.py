from django.http import HttpResponse
from django.shortcuts import redirect, render

from .models import User

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

from .utils import execute_spotify_api_request, is_spotify_authenticated, update_or_create_token

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

# Create your views here.


@csrf_exempt
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
                    # establishes a session, will add user object as attribute
                    # on request objects, for all subsequent requests until logout
                    user = auth.authenticate(email=email, password=password)
                    if user is not None:
                        auth.login(request, user)
                        return Response({'status': 'logged_in'}, status=status.HTTP_200_OK)
                    else:
                        return Response({'status': 'user_somehow_none??'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response({'status': 'user_already_exists'}, status=status.HTTP_409_CONFLICT)
            else:
                return Response({'status': 'invalid_form'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': 'invalid_method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    except NameError:
        return Response({'status': 'backend_name_error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
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
                # establishes a session, will add user object as attribute
                # on request objects, for all subsequent requests until logout
                user = auth.authenticate(email=email, password=password)
                if user is not None:
                    auth.login(request, user)
                    return Response({'status': 'logged_in'}, status=status.HTTP_200_OK)
                else:
                    return Response({'status': 'user_somehow_none??'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({'status': 'user_already_exists'}, status=status.HTTP_409_CONFLICT)
        else:
            return Response({'status': 'invalid_method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    except NameError:
        return Response({'status': 'backend_name_error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(('POST',))
def login(request):

    form = LoginForm()

    try:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user = auth.authenticate(email=email, password=password)
                if user is not None:
                    auth.login(request, user)
                    return Response({'status': 'logged_in'}, status=status.HTTP_200_OK)
                else:
                    # failed authentication
                    return Response({'status': 'invalid_credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                # invalid form
                return Response({'status': 'invalid_form'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': 'invalid_method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    except NameError:
        return Response({'status': 'backend_name_error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(('POST',))
def logout(request):
    auth.logout(request)
    return Response({'status': 'logged_out'}, status=status.HTTP_200_OK)


class AuthURL(APIView):
    def get(self, request, format=None):
        print("We are authorising, nothing fancy and no tokens set")
        scopes = 'user-library-modify user-library-read app-remote-control playlist-modify-public'

        url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope': scopes,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
        }).prepare().url
        print("Successfully achieved an authorisation response")

        return Response({'url': url}, status=status.HTTP_200_OK)


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class SpotifyTest(APIView):
    def get(self, request, format=None):
        response = execute_spotify_api_request(
            session_id=self.request.session.session_key,
            endpoint="playlists/1aGCxSHK4noZhGVa961sD2/tracks")
        return Response(
            data=response)


def spotify_callback(request, format=None):
    code = request.GET.get('code')
    error = request.GET.get('error')

    print("We have been directly redirected, from here we're going to gather information and I will display this all")

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
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
        request.session.session_key, access_token, token_type, expires_in, refresh_token)

    return redirect('test_spotify_api')


class IsAuthenticated(APIView):
    def get(self, request, format=None):
        is_authenticated = is_spotify_authenticated(
            self.request.session.session_key)
        return Response({'status': is_authenticated}, status=status.HTTP_200_OK)
