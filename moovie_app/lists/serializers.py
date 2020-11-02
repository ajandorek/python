from rest_framework import serializers, validators
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password

from lists.models import Genre, Movie, List, Video, MoovieUser


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name')


class MovieSerializer(serializers.HyperlinkedModelSerializer):
    genres = GenreSerializer(many=True)
    class Meta:
        model = Movie
        fields = ('id', 'title', 'tagline', 'overview', 'release_date',
                  'poster_url', 'backdrop_url', 'imdb_id', 'genres')


class CreateUserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = MoovieUser
        fields = ['id', 'email', 'full_name', 'photo_path', 'password']
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        user = super(CreateUserSerializer, self).create(validated_data)
        if user:
            send_mail('Welcome to the Moovie App!', 'Welcome to the movie app %s' % user.full_name, 'moovieapp15@gmail.com',
                      [user.email], fail_silently=False)

        return user


class GetUsersSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MoovieUser
        fields = ['id', 'full_name', 'email', 'photo_path']

class VideoSerializer(serializers.HyperlinkedModelSerializer):
    movie = MovieSerializer(many=True)
    class Meta:
        model = Video
        fields = ['size', 'type', 'url', 'movie']

class ListSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(default=serializers.CreateOnlyDefault(serializers.CurrentUserDefault()))

    movies = MovieSerializer(many=True)
    class Meta:
        model = List
        fields = ('name', 'description', 'public', 'owner', 'movies',)
