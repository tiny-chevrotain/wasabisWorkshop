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
    path('secret-signup/', views.guest_signup, name='secret_login'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('get-auth-url/', views.AuthURL.as_view(), name='get_auth_url'),
    path('is-authenticated/', views.IsAuthenticated.as_view(),
         name='is_authenticated'),
    path('test-spotify-api/', views.SpotifyTest.as_view(),
         name='test_spotify_api'),
    path('redirect/', views.spotify_callback, name='redirect')
]
