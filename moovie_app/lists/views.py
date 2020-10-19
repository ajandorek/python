from django.shortcuts import render
from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
import django_filters.rest_framework
from rest_framework import filters


from lists.serializers import GenreSerializer, MovieSerializer
from lists.models import Genre, Movie

# Create your views here.


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.rest_framework.DjangoFilterBackend]
    ordering_fields = ['title', 'genres__name', 'imdb_id']
    search_fields = ['title', 'genres__name']

    def get_queryset(self):
        queryset = Movie.objects.all()
        genre = self.request.query_params.get('genres', None)
        title = self.request.query_params.get('title', None)
        if genre is not None:
            queryset = queryset.filter(genre=genre)
        elif title is not None:
            queryset = queryset.filter(title=title)
        return queryset
