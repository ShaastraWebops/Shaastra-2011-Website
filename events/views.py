from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.template.loader import get_template
from django.template.context import Context, RequestContext

from main_test.misc.util import *
from main_test.settings import *
from main_test.users.models import User

import forms, models

import datetime

import os

#I m _not_ writing templates write now. Just creating empty html files. 
def show_quick_tab(request):
    data=QuickTab.objects.all()
    event_name,title,text=data.event.name,data.title,data.text
    return render_to_response('events/QuickTabs.html', locals(), context_instance= global_context(request)) 

