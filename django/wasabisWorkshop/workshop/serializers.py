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
        depth = 1


class ScoreSerializer(serializers.ModelSerializer):
    song = SongSerializer(read_only=True)

    class Meta:
        model = Score
        fields = ['id', 'upvotes_count', 'downvotes_count',
                  'votes_total', 'song']


class UpvoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upvote
        fields = ['score', 'user']


class DownvoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Downvote
        fields = ['score', 'user']


class WasabiaSerializer(serializers.ModelSerializer):
    scores = ScoreSerializer(many=True, read_only=True)

    class Meta:
        model = Wasabia
        fields = ['id', 'name', 'description', 'scores']
        depth = 1


class WasabiaInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wasabia
        fields = ['id', 'name', 'description',
                  'votes', 'song_count', 'image']
        depth = 2
