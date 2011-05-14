from django.http import httpresponse
from dajngo.shortcuts import render_to_response
from django.template.loader import get_template
from django.template.context import Context, RequestContext
from main_test.users.models import *

import forms, models

