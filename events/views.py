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
<<<<<<< HEAD
    return render_to_response('events/QuickTabs.html', locals(), context_instance= global_context(request)) 
   
        
def edit_content(request,event_name = None,title)
    
    user = request.user
    userprof = user.get_profile()
    events_list = models.Event.objects.filter(registerable=True)
    
    #invalid 
    if e_name is None or e_name == '':  
    
    # to be redirected to appropriate page
    else:
    
    	e_name = decamelize(e_name)   
        e_name = e_name.replace('/','')
        
        if not events_list.filter(name=event_name): 
        # to be redirected to appropriate page
        else:
        
        	coord_list = models.coord.objects.filter(event_name = event_name)
        	if not user in coord_list:
        	#redirect to appropriate page
        	else:
        	
        		if request.method == 'POST':
        			data = request.POST.copy()
        			form = forms.EditData(data)
        			qtab = models.QuickTab.objects.filter(title = title, event = event_name)
        			if form.is_valid():
        				text = form.cleaned_data["text"]
        				qtab.text = text
       
        				
=======
    return render_to_response('events/QuickTabs.html', locals(), context_instance= global_context(request))

# here is my idea of adding new tab
# # i presume there will be a button say add tab
#  once that is clicked a form will come asking for name of tab
#  the user fills the title for tab in it
#  someone please correct me if i am wrong
@needs_authentication
@coords_only
def add_quick_tabs(request):
	if request.method=='GET':
		data=request.GET.copy()
		form = forms.AddTabForm(data)

		
			title=form.cleaned_data['title']
			return render_to_response('events/QuickTabs.html', locals(), context_instance= global_context(request))
	
	

	


>>>>>>> 166d7acb09545fe1c9ae4208690b4f67f00ef5db
