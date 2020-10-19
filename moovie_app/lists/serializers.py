from rest_framework import serializers

from lists.models import Genre, Movie

class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name')

class MovieSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'title', 'tagline', 'overview', 'release_date', 'poster_url', 'backdrop_url', 'imdb_id', 'genre')