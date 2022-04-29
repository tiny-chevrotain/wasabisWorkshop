import json
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .test_personalisation import test_spotify_functionality

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

from .utils import authenticate_user, execute_spotify_api_request, is_spotify_authenticated, update_or_create_token

from rest_framework.decorators import api_view, renderer_classes, authentication_classes, permission_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

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
@permission_classes((IsAuthenticated,))
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
@permission_classes((IsAuthenticated,))
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


@csrf_exempt
@api_view(('GET',))
def test(request):
    response = test_spotify_functionality()

    # with open('workshop/personalise_test.json', 'w') as f:
    #     json.dump(response, f)

    # new_items = []
    # for item in response['items']:
    #     item['track'].pop('available_markets', None)
    #     item['track']['album'].pop('available_markets', None)
    #     new_items.append(item)
    # response.update({'items': new_items})

    return Response(response, status=status.HTTP_200_OK)
# # hopefully this runs at compile time?
# for user in User.objects.all():
#     Token.objects.get_or_create(user=user)
