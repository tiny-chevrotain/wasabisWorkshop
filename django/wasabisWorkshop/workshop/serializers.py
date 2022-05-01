from rest_framework import serializers

from .models import User, Artist, Song, Score, Upvote, Downvote, Wasabia


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name']


class ArtistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Artist
        fields = ['id', 'name']


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id', 'name', 'artists', 'image_640_url',
                  'image_300_url', 'image_64_url']


class ScoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Score
        fields = ['id', 'upvotes_count', 'downvotes_count',
                  'votes_total', 'song', 'wasabia']


class UpvoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upvote
        fields = ['score', 'user']


class DownvoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Downvote
        fields = ['score', 'user']


class WasabiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wasabia
        fields = ['id', 'name', 'description',
                  'songs', 'user', 'votes', 'scores']
        depth = 1
