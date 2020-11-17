from rest_framework import serializers, validators
from django.contrib.auth import get_user_model, models
from django.core.mail import send_mail

from lists.models import Genre, Movie, List, Video


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name')


class MovieSerializer(serializers.HyperlinkedModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    class Meta:
        model = Movie
        fields = ('id', 'title', 'tagline', 'overview', 'release_date',
                  'poster_url', 'backdrop_url', 'imdb_id', 'genres')


class CreateUserSerializer(serializers.HyperlinkedModelSerializer):
    email = serializers.EmailField(required=True, validators=[
                                   validators.UniqueValidator(queryset=models.User.objects.all())])
    username = serializers.CharField(
        validators=[validators.UniqueValidator(queryset=models.User.objects.all())])
    password = serializers.CharField(min_length=8, style={
                                     "input_type": "password"}, write_only=True, label="Password")

    def create(self, validated_data):
        user = models.User.objects.create_user(
            validated_data['username'], validated_data['email'], validated_data['password'])

        if user:
            send_mail('Welcome to the Moovie App!', 'Welcome to the movie app %s' % user.username, 'moovieapp15@gmail.com',
                      [user.email], fail_silently=False)

        return user

    class Meta:
        model = models.User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {"password": {"write_only": True}}


class GetUsersSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'username', 'email']

class VideoSerializer(serializers.HyperlinkedModelSerializer):
    movie = MovieSerializer(read_only=True)
    class Meta:
        model = Video
        fields = ['size', 'type', 'url', 'movie']

class ListSerializer(serializers.HyperlinkedModelSerializer):
    movies = MovieSerializer(many=True, read_only=True)
    class Meta:
        model = List
        fields = ['name', 'description', 'public', 'movies']
