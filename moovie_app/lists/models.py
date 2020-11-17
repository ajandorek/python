from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager
# Create your models here.


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ('id', )

    def __str__(self):
        return f'{self.name}'


class Movie(models.Model):
    title = models.CharField(max_length=50, unique=True)
    tagline = models.CharField(max_length=100)
    overview = models.CharField(max_length=250, blank=True)
    release_date = models.DateField()
    poster_url = models.CharField(max_length=100)
    backdrop_url = models.CharField(max_length=100)
    imdb_id = models.CharField(max_length=10)
    genres = models.ManyToManyField(Genre)

    class Meta:
        ordering = ('id', )

    def __str__(self):
        return f'{self.title}'

class Video(models.Model):
    size = models.IntegerField()
    type = models.CharField(max_length=50)
    url = models.CharField(max_length=100)
    movie = models.ForeignKey(Movie, on_delete=models.PROTECT, related_name='movie', null=True)

class List(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    public = models.BooleanField()
    movies = models.ManyToManyField(Movie, blank=True)
    owner = models.ForeignKey('MoovieUser', related_name='+', on_delete=models.PROTECT, null=True)

    class Meta:
        ordering = ('id', )

    def __str__(self):
        return f'{self.name}'

class MoovieUser(AbstractUser):
    username = None
    email = models.CharField(max_length=50, unique=True)
    lists = models.ManyToManyField(List)
    full_name = models.CharField(max_length=100)
    photo_path = models.CharField(max_length=100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    class Meta:
        ordering = ('id', )

    def __str__(self):
        return self.email
