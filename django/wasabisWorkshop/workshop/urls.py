"""wasabisWorkshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import views
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', views.index, name='index'),

    # user authentication:
    path('login/', views.login, name='login'),
    path('token-login/', views.token_login, name='token_login'),
    path('signup/', views.signup, name='signup'),
    path('secret-signup/', views.guest_signup, name='secret_login'),
    path(
        'is-authenticated/',
        views.IsAuthenticated.as_view(),
        name='is_authenticated',
    ),
    path(
        'spotify-create-token/',
        views.spotify_create_token,
        name='spotify_create_token',
    ),

    # system API:
    path(
        'test-spotify-api/',
        views.SpotifyTest.as_view(),
        name='test_spotify_api',
    ),
    path(
        'get-recommendations/',
        views.get_recommendations,
        name='get_recommendations',
    ),
    path(
        'get-wasabia-list/',
        views.get_wasabia_list,
        name='get_wasabia_list',
    ),
    path(
        'create-wasabia/',
        views.create_wasabia,
        name='create_wasabia',
    ),
    path(
        'get-wasabia/',
        views.get_wasabia,
        name='get_wasabia',
    ),
    path(
        'add-songs/',
        views.add_songs,
        name='add_songs',
    ),
    path(
        'search-spotify/',
        views.search_spotify,
        name='search_spotify',
    ),
    path(
        'get-playlists/',
        views.get_playlists,
        name='get_playlists',
    ),
    path(
        'get-user-library/',
        views.get_user_library,
        name='get_user_library',
    ),
    path(
        'get-user-saved-songs/',
        views.get_user_saved_songs,
        name='get_user_saved_songs',
    ),
    path(
        'get-user-playlist-songs/',
        views.get_user_playlist_songs,
        name='get_user_playlist_songs',
    ),
    path(
        'song-vote/',
        views.song_vote,
        name='song_vote',
    ),

    # path('test', views.test, name='test'),
]
