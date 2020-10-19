from django.db import models

# Create your models here.


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ('id', )
    
    def __str__(self):
        return f'{self.name}'

class Movie(models.Model):
    title = models.CharField(max_length=50)
    tagline = models.CharField(max_length=100)
    overview = models.CharField(max_length=250, blank=True)
    release_date = models.DateField()
    poster_url = models.CharField(max_length=100)
    backdrop_url = models.CharField(max_length=100)
    imdb_id = models.CharField(max_length=10)
    genre = models.ForeignKey(
        Genre, on_delete=models.PROTECT, to_field='name')

    class Meta:
        ordering = ('id', )
    
    def __str__(self):
        return f'{self.title}{self.id}{self.genre}{self.imdb_id}'
