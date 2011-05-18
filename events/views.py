from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.template.loader import get_template
from django.template.context import Context, RequestContext

from main_test.misc.util import *               #Importing everything - just in case
from main_test.settings import *
from main_test.users.models import User
from main_test.events.models import *
from main_test.events.forms import *
from main_test.submissions.models import *    
from main_test.submissions.forms import *

import datetime

import os

#We can check if coords are logged in using the request.session['logged_in'] variable and then allow them to edit the corresponding event page after verifying this.
def coordslogin (request)
    form=forms.CoordLoginForm()
    if request.method == 'POST':
        data = request.POST.copy()
        form = forms.CoordLoginForm(data)
        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data["password"])
            if user is not None and user.is_active == True:
                auth.login (request, user)
                request.session['logged_in'] = True
                url="%s/coordhome/"%settings.SITE_URL
                #This URL can be changed as required later
                response= HttpResponseRedirect (url)
                return response
            else:
                request.session['invalid_login'] = True
                request.session['logged_in'] = False
                url="%s/coordlogin"%settings.SITE_URL
                #This URL can be changed as required later
                response= HttpResponseRedirect (url)
                return response
        else:                       
            invalid_login = session_get(request, "invalid_login")
            form = forms.UserLoginForm () 
    return render_to_response('events/coordlogin.html', locals(), context_instance= global_context(request))
    #This URL can be changed as required later
                   
#I m _not_ writing templates write now. Just creating empty html files. 
def show_quick_tab(request,event_name=None):
    data=QuickTab.objects.all()
    event_name,title,text=data.event.name,data.title,data.text
    return render_to_response('events/QuickTabs.html', locals(), context_instance= global_context(request)) 


# here is my idea of adding new tab
# # i presume there will be a button say add tab
#  once that is clicked a form will come asking for name of tab
#  the user fills the title for tab in it
#  someone please correct me if i am wrong
@needs_authentication
@coords_only
def add_quick_tabs(request,event_name = None):
    #just a check if the coord is viewing the right page...
    
    user=request.user
    userprof=user.get_profile()
    events_list = models.Event.objects.filter(registerable=True)
    
    if event_name is None or event_name == "":
        #the url can be changed later
        return HttpResponseRedirect ('%s/events/'%settings.SITE_URL)
    #check if events name is there in the list
    else if:
        event_name=decamelize(event_name)
        event_name=event_name.replace('/','')
        if not events_list.filter(name=event_name): 
            request.session ['invalid_event'] = event_name
            return HttpResponseRedirect ('%s/events/'%settings.SITE_URL)
    
    else if:
        coord_list = models.coord.objects.filter(event_name = event_name)
        if not user in coord_list:
            return HttpResponseRedirect ('%s/events/'%settings.SITE_URL)
    
    else:
        if request.method=='GET': # get or post  ????
            data=request.GET.copy()
            form = forms.AddTabForm(data)
            title=form.cleaned_data['title']
            event = event_name
            text = form.cleaned_data['text']
            return render_to_response('events/QuickTabs.html', locals(), context_instance= global_context(request))
        
        
def remove_quick_tab(request,event_name = None,title):

    user=request.user
    userprof=user.get_profile()
    
    if event_name is None or event_name == "":
        #the url can be changed later
        return HttpResponseRedirect ('%s/events/'%settings.SITE_URL)
    #check if events name is there in the list
    else if:
        event_name=decamelize(event_name)
        event_name=event_name.replace('/','')
        if not events_list.filter(name=event_name): 
            request.session ['invalid_event'] = event_name
            return HttpResponseRedirect ('%s/events/'%settings.SITE_URL)
    
    else if:
        coord_list = models.coord.objects.filter(event_name = event_name)
        if not user in coord_list:
            return HttpResponseRedirect ('%s/events/'%settings.SITE_URL)
            
    else:
        if request.method == 'GET':
            tab=models.QuickTab.objects.filter(event_name = event_name)
            tab.delete()
            return render_to_response('events/QuickTabs.html', locals(), context_instance= global_context(request))
            
            

def edit_content(request,event_name = None,title)

    user=request.user
    userprof=user.get_profile()
    
    if event_name is None or event_name == "":
        #the url can be changed later
        return HttpResponseRedirect ('%s/events/'%settings.SITE_URL)
    #check if events name is there in the list
    else if:
        event_name=decamelize(event_name)
        event_name=event_name.replace('/','')
        if not events_list.filter(name=event_name): 
            request.session ['invalid_event'] = event_name
            return HttpResponseRedirect ('%s/events/'%settings.SITE_URL)
    
    else if:
        coord_list = models.coord.objects.filter(event_name = event_name)
        if not user in coord_list:
            return HttpResponseRedirect ('%s/events/'%settings.SITE_URL)
            
    else:
        if request.method == 'POST':
            data = request.POST.copy()
            form = forms.EditData(data)
            qtab = models.QuickTab.objects.filter(title = title, event = event_name)
            if form.is_valid():
                text = form.cleaned_data["text"]
                qtab.text = text



    return render_to_response('events/QuickTabs.html', locals(), context_instance= global_context(request))
