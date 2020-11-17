from django.shortcuts import render
from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
import django_filters.rest_framework
from rest_framework import filters, mixins
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage

from lists.serializers import GenreSerializer, MovieSerializer, CreateUserSerializer, GetUsersSerializers
from lists.models import Genre, Movie

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

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = get_user_model().objects.all()
    serializer_class = GetUsersSerializers

class CreateUserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = CreateUserSerializer
