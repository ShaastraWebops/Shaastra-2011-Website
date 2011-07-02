from haystack.indexes import *
from haystack import site
from main_test.events.models import Event

class EventIndex(SearchIndex):
    text = CharField(document=True, use_template=True)

site.register(Event, EventIndex)
