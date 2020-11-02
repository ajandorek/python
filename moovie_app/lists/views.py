from django.shortcuts import render
from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
import django_filters.rest_framework
from rest_framework import filters, mixins
from django.core.mail import EmailMessage
from json import dumps, loads, JSONEncoder

from lists.serializers import GenreSerializer, MovieSerializer, CreateUserSerializer, GetUsersSerializers, ListSerializer, VideoSerializer
from lists.models import Genre, Movie, List, Video, MoovieUser

# Create your views here.


class GenreViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class MovieViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.rest_framework.DjangoFilterBackend]
    ordering_fields = ['title', 'genres__name', 'imdb_id']
    search_fields = ['title', 'genres__name']

    def get_queryset(self):
        queryset = Movie.objects.all()
        genres = self.request.query_params.get('genres', None)
        title = self.request.query_params.get('title', None)
        if genres is not None:
            queryset = queryset.filter(genres__name=genres)
        elif title is not None:
            queryset = queryset.filter(title__contains=title)
        return queryset


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = MoovieUser.objects.all()
    serializer_class = GetUsersSerializers

    @action(detail=True, methods=['post'])
    def delete_profile_photo(self, request, pk):
        current_user = self.get_object()
        current_user.photo_path = ''
        current_user.save()
        serializer = self.get_serializer(current_user)

        return Response(serializer.data)

    @action(detail=True, methods=['put'])
    def update_profile_photo(self, request, pk):
        current_user = self.get_object()
        photo_path = request.data["photo_path"]
        current_user.photo_path = photo_path
        current_user.save()
        serializer = self.get_serializer(current_user)

        return Response(serializer.data)


class CreateUserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = MoovieUser.objects.all()
    serializer_class = CreateUserSerializer


class VideoViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class ListViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = List.objects.all()
    serializer_class = ListSerializer

    @action(detail=True, methods=['post'])
    def delete_movie(self, request, pk):
        current_list = self.get_object()
        for key in request.data["movies"]:
            if type(key) == int:
                update_movies = current_list.movies.all().exclude(id=key)
                current_list.movies.set(update_movies)
            elif type(key) == str:
                update_movies = current_list.movies.all().exclude(title=key)
                current_list.movies.set(update_movies)
        current_list.save()
        serializer = self.get_serializer(current_list)

        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_movie(self, request, pk):
        current_list = self.get_object()
        for key in request.data["movies"]:
            if type(key) == int:
                queryset = Movie.objects.all()
                filtered_movie = queryset.filter(id=key)
                filtered_movie |= current_list.movies.all()
                current_list.movies.set(filtered_movie)
            elif type(key) == str:
                queryset = Movie.objects.all()
                filtered_movie = queryset.filter(title=key)
                filtered_movie |= current_list.movies.all()
                current_list.movies.set(filtered_movie)
        current_list.save()
        serializer = self.get_serializer(current_list)

        return Response(serializer.data)
