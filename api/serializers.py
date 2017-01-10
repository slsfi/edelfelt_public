
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
import urllib
from EdelfeltApp.models import Letter, Person, Event, Artwork, File, ArtworkFile, Location
from django.templatetags.static import static

HOST = 'http://URL'

class PersonSerializer(serializers.HyperlinkedModelSerializer):
    type = serializers.SerializerMethodField()
    web_url = serializers.SerializerMethodField()
    nobiliary_particle = serializers.CharField(source='von_van_af')
    id = serializers.IntegerField(source='fm_id')

    name_2 = serializers.CharField(source='name_2_display')
    name_info_2 = serializers.CharField(source='name_info2')
    url = serializers.HyperlinkedIdentityField(view_name='person-detail', lookup_field='fm_id')

    class Meta:
        model = Person
        fields = ('url', 'id', 'name', 'first_name', 'last_name', 'nobiliary_particle', 'birth_year', 'death_year',
                  'description', 'source', 'type', 'web_url', 'name_info', 'name_2', 'name_info_2', 'events')

    def get_web_url(self, obj):
        return append_url(obj.get_absolute_url())

    events = serializers.HyperlinkedRelatedField(
        view_name='event-detail',
        lookup_field='fm_id',
        read_only=True,
        many=True,
    )

    def get_type(self, obj):
        TYPE_CHOICES = (
            ('1', 'contemporary'),
            ('2', 'mythological'),
            ('3', 'historical')
        )
        for choice in TYPE_CHOICES:
            if choice[0] == obj.type:
                return choice[1]


class YearListingField(serializers.RelatedField):
    def to_representation(self, value):
        return value.start_year_no

class MonthListingField(serializers.RelatedField):
    def to_representation(self, value):
        return value.start_month_no

class DayListingField(serializers.RelatedField):
    def to_representation(self, value):
        return value.start_day_no

class EventSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(source='fm_id')
    year = YearListingField(source='letter', read_only=True)
    month = MonthListingField(source='letter', read_only=True)
    day = DayListingField(source='letter', read_only=True)

    letter = serializers.HyperlinkedRelatedField(
        view_name='letter-detail',
        lookup_field='fm_id',
        read_only=True
    )

    persons = serializers.HyperlinkedRelatedField(
        view_name='person-detail',
        lookup_field='fm_id',
        read_only=True,
        many=True
    )

    mentioned_locations = serializers.HyperlinkedRelatedField(
        view_name='location-detail',
        lookup_field='fm_id',
        read_only=True,
        many=True
    )

    artworks = serializers.HyperlinkedRelatedField(
        view_name='artwork-detail',
        lookup_field='fm_id',
        read_only=True,
        many=True
    )

    url = serializers.HyperlinkedIdentityField(view_name='event-detail', lookup_field='fm_id')

    class Meta:
        model = Event
        fields = ('url', 'id', 'title', 'letter', 'order', 'persons', 'artworks', 'year', 'month', 'day', 'mentioned_locations')


class LocationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='fm_id')

    url = serializers.HyperlinkedIdentityField(view_name='location-detail', lookup_field='fm_id')

    events = serializers.HyperlinkedRelatedField(
        view_name='event-detail',
        lookup_field='fm_id',
        read_only=True,
        many=True,
    )

    class Meta:
        model = Location
        fields = ('url', 'id', 'name', 'country', 'province', 'lat', 'long', 'comment', 'events')

class LetterFileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='fm_id')

    large = serializers.SerializerMethodField()

    def get_large(self, obj):
        return append_url(static(obj.path))

    thumbnail = serializers.SerializerMethodField()
    def get_thumbnail(self, obj):
        return append_url(static(obj.thumb_path))

    class Meta:
        model = File
        fields = ('id', 'large', 'thumbnail')

class LetterSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(source='fm_id')
    url = serializers.HyperlinkedIdentityField(view_name='letter-detail', lookup_field='fm_id')

    events = serializers.HyperlinkedRelatedField(
        view_name='event-detail',
        lookup_field='fm_id',
        read_only=True,
        many=True,
    )

    locations = serializers.HyperlinkedRelatedField(
        view_name='location-detail',
        lookup_field='fm_id',
        read_only=True,
        many=True,
    )

    #events = EventSerializer(many=True)

    pages = LetterFileSerializer(many=True, source='files')

    web_url = serializers.SerializerMethodField()

    def get_web_url(self, obj):
        return append_url(obj.get_absolute_url())

    class Meta:
        model = Letter
        lookup_field = 'fm_id'
        fields = ('url', 'id', 'title', 'events', 'web_url', 'date', 'urn', 'pages', 'events', 'locations')
        depth = 1



class PictureSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='fm_id')
    url = serializers.HyperlinkedIdentityField(view_name='picture-detail', lookup_field='fm_id')
    type = serializers.SerializerMethodField()
    fng_id = serializers.SerializerMethodField()
    fng_url = serializers.SerializerMethodField()
    fng_api_url = serializers.SerializerMethodField()

    artwork =  serializers.HyperlinkedRelatedField(
        view_name='artwork-detail',
        lookup_field='fm_id',
        read_only=True)

    def get_fng_id(self, obj):
        return obj.file.esinetunnus

    def get_fng_url(self, obj):
        return obj.file.fng_url()

    def get_fng_api_url(self, obj):
        apikey = '[FNG_APIKEY]'
        api_url = str.format('http://kokoelmat.fng.fi/api/v2?&q={0}&apikey={1}&format=dc-json', urllib.quote_plus(obj.file.esinetunnus), apikey)
        print api_url
        #return urllib.urlencode(api_url)
        return api_url

    def get_type(self, obj):
        TYPE_CHOICES = (
            ('0', ''),
            ('1', 'Main work'),
            ('2', 'Sketch'),
            ('3', 'Uncertain sketches'),
            ('4', 'Related works and sketches'),
            ('5', 'Related work'),
            ('6', 'Uncertain'),
        )
        for choice in TYPE_CHOICES:
                if choice[0] == obj.type:
                    return choice[1]

    class Meta:
        model = ArtworkFile
        fields = ('id', 'url', 'artwork', 'type', 'fng_id', 'fng_url', 'fng_api_url')



class ArtworkSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(source='fm_id')

    events = serializers.HyperlinkedRelatedField(
        view_name='event-detail',
        lookup_field='fm_id',
        read_only=True,
        many=True,
    )

    pictures = serializers.HyperlinkedRelatedField(
        view_name='picture-detail',
        lookup_field='fm_id',
        read_only=True,
        many=True,
        source='artworkfiles'
    )

    web_url = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(view_name='artwork-detail', lookup_field='fm_id')

    def get_web_url(self, obj):
        return append_url(obj.get_absolute_url())


    class Meta:
        model = Artwork
        lookup_field = 'fm_id'
        fields = ('url', 'id', 'title', 'title2', 'title3', 'title4', 'web_url', 'comments', 'type', 'events', 'pictures')


def append_url(url):
    if len(url) > 0 and url[0] != '/':
        url = '/' + url

    return HOST + url