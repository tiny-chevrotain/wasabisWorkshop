from django.contrib import admin

from .models import Artist, Downvote, Score, Song, Upvote, User, Wasabia


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # 'wasabias', 'upvotes', 'downvotes'
    list_display = ['id', 'email', 'name']


@admin.register(Wasabia)
class WasabiaAdmin(admin.ModelAdmin):
    filter_horizontal = ('songs',)
    list_display = ['id', 'name', 'description', 'user']  # 'songs',


@admin.register(Artist)
class SongAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    filter_horizontal = ('artists',)
    list_display = ['id', 'name']


@admin.register(Upvote)
class UpvoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'score', 'user']


@admin.register(Downvote)
class DownvoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'score', 'user']  # 'user',


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ['id', 'song', 'wasabia']
    # filter_horizontal = ('upvotes', 'downvotes')
