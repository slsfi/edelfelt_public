__author__ = 'dennis'

from django.conf.urls import url, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()

router.register(r'persons', views.Person)
router.register(r'letters', views.Letter)
router.register(r'events', views.Event)
router.register(r'artworks', views.Artwork)
router.register(r'pictures', views.Picture, base_name='picture')
router.register(r'locations', views.Location)
#router.register(r'events', views.EventViewSet, base_name='event')

urlpatterns = [
    url(r'^', include(router.urls)),
    ]