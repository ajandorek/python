from django.test import TestCase
from django.urls import reverse
from lists.models import Genre
from lists.views import GenreViewSet
from faker import Faker
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework.views import status

# Create your tests here.

# Genre Tests
class GenreTestCase(TestCase):
  def test_genre(self):
    self.assertEquals(Genre.objects.count(), 0)
    Genre.objects.create(name='Action')
    self.assertEquals(Genre.objects.count(), 1)

class GenreAPIViewTest(APITestCase):
  def setUp(self) -> None:
    self.url = reverse('genre-list')
    self.genre = Genre.objects.create(name='Comedy')

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
      response = self.client.get(url)
      self.assertEquals(
          response.status_code,
          status.HTTP_200_OK
      )
      data = response.json()
      data['name'] = 'Comedy'
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
