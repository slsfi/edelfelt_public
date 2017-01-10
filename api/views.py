from django.shortcuts import render
from EdelfeltApp.models import Person, Event, Letter, Artwork, ArtworkFile, Location
from rest_framework import viewsets,filters
from api.serializers import PersonSerializer, EventSerializer, LetterSerializer, ArtworkSerializer, PictureSerializer, LocationSerializer
import django_filters
import requests
from django.views.decorators.cache import never_cache

# Create your views here.



def ReportAnalytics(action, objectType, objectId):

    if objectId != '':
        payload = str.format('', action, objectType, objectId)
    else:
        payload = str.format('', action, objectType)
    r = requests.post('http://www.google-analytics.com/collect', data=payload)


class PersonFilter(django_filters.FilterSet):
    connected_person_id = django_filters.CharFilter(name="events__persons__fm_id", distinct=True)
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'type', 'connected_person_id']

class AnalyticsReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    def list(self, request, *args, **kwargs):
        ReportAnalytics('list', type(self).__name__, '')
        return super(AnalyticsReadOnlyModelViewSet, self).list(self, request, *args, **kwargs)

    def retrieve(self, request, pk=None, *args, **kwargs):
        fm_id = kwargs.get(u'fm_id', '')
        ReportAnalytics('retrieve', type(self).__name__, fm_id)
        return super(AnalyticsReadOnlyModelViewSet, self).retrieve(self, request, pk, *args, **kwargs)


class Person(AnalyticsReadOnlyModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    lookup_field = 'fm_id'
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter)
    search_fields= ['first_name', 'last_name', 'von_van_af', 'name_2_display', 'name_3_display', 'name_4_display', 'alternative_name', 'nickname', 'description']
    filter_class = PersonFilter

class EventFilter(django_filters.FilterSet):
    connected_person_id = django_filters.CharFilter(name="persons__fm_id", distinct=True)
    mentioned_location_id = django_filters.CharFilter(name="mentioned_locations__fm_id", distinct=True)
    year = django_filters.NumberFilter(name="letter__start_year_no", distinct=True)
    month = django_filters.NumberFilter(name="letter__start_month_no", distinct=True)
    day = django_filters.NumberFilter(name="letter__start_day_no", distinct=True)

    class Meta:
        model = Event

        fields = ['connected_person_id', 'year', 'month', 'day']


class Event(AnalyticsReadOnlyModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = 'fm_id'
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter)
    filter_class = EventFilter
    search_fields= ['title',]

class LetterFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter(name="start_year_no", distinct=True)
    month = django_filters.NumberFilter(name="start_month_no", distinct=True)
    day = django_filters.NumberFilter(name="start_day_no", distinct=True)
    location_id = django_filters.CharFilter(name="locations__fm_id", distinct=True)

    class Meta:
        model = Letter
        fields = ['year', 'month', 'day', 'location_id']

class Letter(AnalyticsReadOnlyModelViewSet):
    queryset = Letter.objects.all()
    serializer_class = LetterSerializer
    lookup_field = 'fm_id'
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter)
    search_fields= ['title',]
    filter_class = LetterFilter

class ArtworkFilter(django_filters.FilterSet):

    class Meta:
        model = Artwork
        fields = ['title', 'title2', 'title3', 'title4']

class Artwork(AnalyticsReadOnlyModelViewSet):
    queryset = Artwork.objects.all()
    serializer_class = ArtworkSerializer
    lookup_field = 'fm_id'
    filter_backends = (filters.SearchFilter,)
    search_fields= ['title', 'title2', 'title3', 'title4', 'comments']

class Picture(viewsets.ReadOnlyModelViewSet):
    queryset = ArtworkFile.objects.all()
    serializer_class = PictureSerializer
    lookup_field = 'fm_id'

class Location(AnalyticsReadOnlyModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    lookup_field = 'fm_id'
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name', 'country', 'province', 'lat', 'long', 'comment']