from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from lists import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'genres', views.GenreViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]
