from haystack.indexes import *
from haystack import site
from main_test.events.models import Event, QuickTabs, Menu

class EventIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    name = CharField(model_attr='display_name')

class QuickTabsIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    content = CharField(model_attr='text')

class MenuIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    
site.register(Event, EventIndex)
site.register(QuickTabs, QuickTabsIndex)
site.register(Menu, MenuIndex)
