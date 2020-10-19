from django.test import TestCase
from django.urls import reverse
from lists.models import Genre, Movie
from django.contrib.auth.models import User
from lists.views import GenreViewSet
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from rest_framework.views import status
from model_bakery import baker
import datetime
from faker import Faker

fake = Faker()
email = fake.email

# Create your tests here.

# Genre Tests
class GenreTestCase(TestCase):
    def test_genre(self):
        self.assertEquals(Genre.objects.count(), 0)
        baker.make(Genre, name='Action')
        self.assertEquals(Genre.objects.count(), 1)


class GenreAPIViewTest(APITestCase):
    def setUp(self) -> None:
        self.url = reverse('genre-list')
        self.genre = baker.make(Genre, name='Comedy')
        self.user = baker.make(User, username='username', email=email, password='username')
        self.client.force_authenticate(user=self.user)

    def test_genre_create_api(self):
        self.assertEquals(Genre.objects.count(), 1)
        data = {'name': 'Action'}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Genre.objects.count(), 2)

    def test_get_genre(self):
        response = self.client.get(self.url)
        response_json = response.json()
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        data = response_json['results'][0]
        self.assertEquals(data['name'], self.genre.name)

    def test_update_genre(self):
        url = reverse('genre-detail', args=[1])
        data = {"name": "Action"}
        response = self.client.put(url, data=data, format='json')
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        self.genre.refresh_from_db()
        self.assertEquals(
            self.genre.name,
            data['name']
        )

    def test_delete_genre(self):
        self.assertEquals(Genre.objects.count(), 1)
        url = reverse('genre-detail', args=[1])
        response = self.client.delete(url)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(Genre.objects.count(), 0)

# Movie Tests


class MovieTestCase(TestCase):
    def test_movie(self):
        self.assertEquals(Genre.objects.count(), 0)
        genre = baker.make(Genre, name='Action')
        baker.make(Movie, title='Test Movie', tagline='Test', overview='overview', release_date='2020-10-12',
                   poster_url='poster.jpg', backdrop_url='background.jpg', imdb_id=1, genres=[genre])
        self.assertEquals(Genre.objects.count(), 1)
        


class MovieAPIViewTest(APITestCase):
    def setUp(self) -> None:
        self.url = reverse('movie-list')
        self.genre = baker.make(Genre, name='Comedy')
        self.movie = baker.make(Movie, title='Test Movie', tagline='Test', overview='overview', release_date='2020-10-12',
                                poster_url='poster.jpg', backdrop_url='background.jpg', imdb_id=1, genres=[self.genre])
        self.user = baker.make(User, username='username', email=email, password='username')
        self.client.force_authenticate(user=self.user)

    def test_movie_create_api(self):
        self.assertEquals(Movie.objects.count(), 1)
        data = {"title": "Test Movie 2", "tagline": "Test", "overview": "overview", "release_date": "2020-10-12",
                "poster_url": "poster.jpg", "backdrop_url": "background.jpg", "imdb_id": "1", "genres": [reverse('genre-detail', args=[1])]}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Movie.objects.count(), 2)

    def test_get_movie(self):
        response = self.client.get(self.url)
        response_json = response.json()
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        data = response_json['results'][0]
        self.assertEquals(data['title'], self.movie.title)

    def test_update_movie(self):
        url = reverse('movie-detail', args=[1])
        data = {"title": "Test Movie 3"}
        response = self.client.patch(url, data=data, format='json')
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        self.movie.refresh_from_db()
        self.assertEquals(
            self.movie.title,
            data['title']
        )

    def test_delete_movie(self):
        self.assertEquals(Movie.objects.count(), 1)
        url = reverse('movie-detail', args=[1])
        response = self.client.delete(url)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(Movie.objects.count(), 0)

    def test_filter_movie(self):
        url = "%s?title=Test" % self.url
        response = self.client.get(url)
        response_json = response.json()
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        data = response_json['results'][0]
        self.assertEquals(data['title'], self.movie.title)

