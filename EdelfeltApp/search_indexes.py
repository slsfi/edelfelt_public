__author__ = 'dennis'
import datetime
from haystack import indexes
from EdelfeltApp.models import Letter, Event, Person, Artwork, Location



class LocationIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)

    def get_model(self):
        return Location

class PersonIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    type = indexes.CharField(model_attr='type',  null=True)
    last_name = indexes.CharField(model_attr='last_name', boost=1.5, null=True) #not sure how boost works, if at all...

    def get_model(self):
        return Person


class LetterIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    start_year_no = indexes.IntegerField(model_attr='start_year_no', null=True)
    start_month_no = indexes.IntegerField(model_attr='start_month_no', null=True)
    #
    # suggestions = indexes.FacetCharField()
    #
    # def prepare(self, obj):
    #     prepared_data = super(LetterIndex, self).prepare(obj)
    #     prepared_data['suggestions'] = prepared_data['text']
    #     return prepared_data

    def get_model(self):
        return Letter


class EventIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)

    def get_model(self):
        return Event



class ArtworkIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)

    def get_model(self):
        return Artwork
