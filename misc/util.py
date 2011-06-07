# Helper functions
from django.contrib import auth
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template.context import Context, RequestContext

from main_test import settings
#from main_test.users import models

import MySQLdb
import re, md5, time

# Some macros for readability
NORMAL = 1
FILE = 2
MCQ = 3
MESSAGE = 4

# Generates a context with the most used variables
def global_context(request):
    is_coord=False
    hospi_coord = False
    is_core = False
    if request.user.is_authenticated() and request.user.groups.filter(name="Coords"):
        is_coord=True
    if request.user.is_authenticated() and request.user.groups.filter(name="HospiCoords"):
        hospi_coord=True
    if request.user.is_authenticated() and request.user.groups.filter(name="EventCores"):
        is_core=True
    context =  RequestContext (request,
            {'user':request.user,
            'SITE_URL':settings.SITE_URL,
            'UNB_URL':settings.SITE_URL,
            'MEDIA_URL':settings.MEDIA_URL,
            'is_coord':is_coord,
            'hospi_coord':hospi_coord,
            'is_core':is_core,
            })
    return context

# Error pages
def not_found (request):
    return render_to_response('404.html', locals(), context_instance= global_context(request)) 
def server_error (request):
    return render_to_response('500.html', locals(), context_instance= global_context(request)) 

#Change FOO   bAR to Foo Bar
def clean_string(dirty_string):
    word_list=dirty_string.split(" ")
    word_list=(s.title().replace('\'S','\'s') for s in word_list)
    cleaned_string=" ".join(word_list)
    return cleaned_string
def clean_state(dir_state):
    str=clean_string(dir_state)
    if str in ["Ap","A.p","A.p.","Andhrapradesh"]:
        return "Andhra Pradesh"
    elif str in ["Up","Uttarpradesh"]:
        return "Uttar Pradesh"
    elif str in ["Tn","Tyamil","Tamilnadu",]:
        return "Tamil Nadu"
    elif str=="J&k":
        return "Jammu And Kashmir"
    elif str== "National Capital Territory Of Delhi":
        return "NCT/Delhi"
    elif str=="Delhi":
        return "NCT/Delhi"
    else :
        return str
def clean_city (dir_city):
    str=clean_string(dir_city)
    if str in ["Hyd"]:
        return "Hyderabad"
    else :
        return str
def clean_colleges():
    college_list=models.College.objects.all()
    for college in college_list:
        college.name=clean_string(college.name) 
        college.state=clean_state(college.state)
        college.city=clean_city(college.city)
        college.save()
# Correct the college value pointed to by the user
def clean_users():
    clean_colleges()
    user_list=models.UserProfile.objects.all()
    for usr in user_list :
        colleges=models.College.objects.filter(name=usr.college.name,city=usr.college.city,state=usr.college.state).order_by("id")
        usr.college=colleges[0]
        usr.save()
#You will have to run only this from a view to clean up colleges.
def cleanup_duplicate():
    clean_users()
    college_list=models.College.objects.order_by("id")
    for college in college_list :
        redundant_list=models.College.objects.filter(name=college.name,city=college.city,state=college.state).order_by("id")
        length=len(redundant_list)
        for i in range(1,length) :
            redundant_list[i].delete()

#sel_college will renamed as new_name
def rename_college(sel_colg,new_name):
    sel_colg.name=new_name
    sel_colg.save()
#sel_college will continue to exist. Colleges in college_list will die!
def merge_colleges(sel_college,college_list):
    user_list=[]
    for col in college_list :
        user_list.extend(models.UserProfile.objects.filter(college=col))
    for usr in user_list :
        usr.college=sel_college
        usr.save()
    for col in college_list :
        if col != sel_college :
            col.delete()

# Convert Foo Contest <-> FooContest
def camelize (str):
    return str.replace (' ','')
def decamelize (str):
    p = re.compile (r'([A-Z][a-z]*)')
    result = ''
    for blob in p.split (str):
        if blob != '':
            result += blob + ' '
    return result[:-1]

# Take care of session variable
def session_get (request, key, default=False):
    value = request.session.get (key, False)
    if value:
        pass
        del request.session[key]
    else: 
        value = default
    return value


# Decorators

# Force authentication first
def needs_authentication (func):
    def wrapper (*__args, **__kwargs):
        request = __args[0]
        if not request.user.is_authenticated():
            # Return here after logging in
            request.session['from_url'] = request.path
            return HttpResponseRedirect ("%sevents/login/"%settings.SITE_URL)
        else:
            return func (*__args, **__kwargs)
    return wrapper

# Check for coords status. Use *after* needs_authentication. Always
def coords_only (func):
    def wrapper (*__args, **__kwargs):
        request = __args[0]
        userprofile= request.user.get_profile()
        if userprofile.is_coord == True:
            return func (*__args, **__kwargs)
        else:
            request.session['access_denied'] = True
            return HttpResponseRedirect ("%s/home/"%settings.SITE_URL)
    return wrapper

# Check for eventcore status. Use *after* needs_authentication. Always
def event_cores_only (func):
    def wrapper (*__args, **__kwargs):
        request = __args[0]
        if request.user.groups.filter(name="EventCores"):
            return func (*__args, **__kwargs)
        else:
            request.session['access_denied'] = True
            return HttpResponseRedirect ("%s/home/"%settings.SITE_URL)
    return wrapper

# Check for admin status. Use *after* needs_authentication. Always
def admin_only (func):
    def wrapper (*__args, **__kwargs):
        request = __args[0]
        if request.user.is_superuser:
            return func (*__args, **__kwargs)
        else:
            request.session['access_denied'] = True
            return HttpResponseRedirect ("%s/home/"%settings.SITE_URL)
    return wrapper

# For urls that can't be accessed once logged in.
def no_login (func):
    def wrapper (*__args, **__kwargs):
        request = __args[0]
        if request.user.is_authenticated():
            # Return here after logging in
            request.session['already_logged'] = True
	    #html = "%s/home/" %SITEURL
            return HttpResponseRedirect ("%s/home/" %settings.SITE_URL)
        else:
            return func (*__args, **__kwargs)
    return wrapper
