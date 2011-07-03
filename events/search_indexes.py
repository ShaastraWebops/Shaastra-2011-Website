from haystack.indexes import *
from haystack import site
from main_test.events.models import Event

class EventIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    url = indexes.CharField(model_attr='url')

site.register(Event, EventIndex)
