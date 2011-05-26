from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.template.loader import get_template
from django.template.context import Context, RequestContext
from django import forms
from main_test.misc.util import *               
from main_test.settings import *
import models,forms

import datetime

import os

#Fileupload is not done perfectly. 
#Desired - Once a file is uploaded page should be refreshed and the uploaded file should be visible as a url link below the textarea

FILE_DIR = '2011/media/main/files/'

#Will change the model after this plan is confirmed
def fileuploadhandler(f,eventname,tabid):
    savelocation = FILE_DIR + eventname + '/' + f.name
    destination = open( savelocation , 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    tab_of_file = models.QuickTabs.objects.get(id=tabid)
    tabfileobject = models.TabFiles (Tab = tab_of_file, url= settings.MEDIA_URL + 'main/files/' + eventname + '/' +f.name)
    tabfileobject.save() 

def coordslogin (request):
    form=forms.CoordsLoginForm()
    if request.method == 'POST':
        data = request.POST.copy()
        form = forms.CoordsLoginForm(data)
        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data["password"])
            if user is not None and user.is_active == True:
                auth.login (request, user)
                request.session['logged_in'] = True
                url="%sevents/dashboard/"%settings.SITE_URL
                #This URL can be changed as required later
                response= HttpResponseRedirect (url)
                return response
            else:
                request.session['invalid_login'] = True
                request.session['logged_in'] = False
                errors=[]
                errors.append("Incorrect username and password combination!")
                return render_to_response('event/login.html', locals(), context_instance= global_context(request))
                
        else:                       
            invalid_login = session_get(request, "invalid_login")
            form = forms.CoordsLoginForm () 
    return render_to_response('event/login.html', locals(), context_instance= global_context(request))
    #This URL can be changed as required later
                   

#Handler for displaying /2011/event/eventname page 
def show_quick_tab(request,event_name=None):
    tab_list=models.QuickTabs.objects.filter(event__name = event_name)
    #for t in tab_list:
        #self.file_list=unicode(models.TabFiles.objects.filter(Tab = self ))
    #So each object in tab_list will have a file_list which is a list of urls to be displayed for the correspdong tab    
    display_edit = False
    if request.method=='POST': 
        user=request.user
        userprof=user.get_profile()
        if userprof.is_coord == True and userprof.coord_event.name == event_name:
            display_edit=True  
    return render_to_response('event/QuickTabs.html', locals(), context_instance= global_context(request)) 

@needs_authentication    
def dashboard(request):

    userprof=request.user.get_profile()
    event_name = userprof.coord_event.name
    tab_list = models.QuickTabs.objects.filter(event__name = event_name)  
    return render_to_response('event/dashboard.html', locals(), context_instance= global_context(request))    

@needs_authentication    
def edit_tab_content(request):

    if request.method=='POST':      
            data=request.POST.copy()
            try:
                form = forms.EditTabForm(data,request.FILES)
            except :  
                form = forms.EditTabForm(data)
            
            if form.is_valid():
                tab_to_edit=models.QuickTabs.objects.get(id=request.session["tab_id"])            
                tab_to_edit.title= form.cleaned_data['title']
                tab_to_edit.text = form.cleaned_data['text']
                tab_to_edit.save()
                fileurllist=unicode(models.TabFiles.objects.filter(Tab = tab_to_edit))
                if request.FILES:
                    userprof=request.user.get_profile()
                    event_name = userprof.coord_event.name
                    fileuploadhandler(request.FILES['tabfile'],event_name,request.session["tab_id"])
                return HttpResponseRedirect ("%sevents/dashboard/"%settings.SITE_URL)            

    else:
        tab_to_edit=models.QuickTabs.objects.get(id=request.GET["tab_id"])
        request.session["tab_id"]=request.GET["tab_id"]
        form = forms.EditTabForm(initial={'title' : tab_to_edit.title , 'text' :tab_to_edit.text, 'tab_pref': tab_to_edit.pref })
        fileurllist=unicode(models.TabFiles.objects.filter(Tab = tab_to_edit))
        #use fileurllist to display the urls of the files associated with each tab
    return render_to_response('event/add_tab.html', locals(), context_instance= global_context(request))
    
@needs_authentication         
def add_quick_tab(request):
    userprof=request.user.get_profile()
    event_name = userprof.coord_event.name
    if request.method=='POST':
        
        data=request.POST.copy()
        if request.FILES:
            form = forms.EditTabForm(data,request.FILES)
        else :
            form = forms.EditTabForm(data)    
        if form.is_valid():
            newtab=models.QuickTabs(title=form.cleaned_data['title'], text=form.cleaned_data['text'], pref=form.cleaned_data['tab_pref'] , event= userprof.coord_event )
            newtab.save()
            if request.FILES:     
                fileuploadhandler(request.FILES["tabfile"],event_name,newtab.id)
            return HttpResponseRedirect ("%sevents/dashboard/"%settings.SITE_URL)
    else:
        form = forms.EditTabForm()
    return render_to_response('event/add_tab.html', locals(), context_instance= global_context(request))    
        
@needs_authentication            
def remove_quick_tab(request):
    tabs_id=request.POST["tab_id"]
    tab_to_delete=models.QuickTabs.objects.filter(id=tabs_id)
    tab_to_delete.delete()
    return HttpResponseRedirect('%sevents/dashboard/'%settings.SITE_URL)

def logout(request):
    if request.user.is_authenticated():
        auth.logout (request)        
        return HttpResponseRedirect('%sevents/login/'%settings.SITE_URL)        

#def handle_uploaded_logo(file_obj, event_id, type_id):
    #try:	
    	#event = models.Event.objects.get(id = event_id)
    #except:
    	#Incomplete
    #if(type_id == 'logo'):
    	#destination = open('%sevent_logos/%s%s'%(FILE_DIR, %event.id), 'wb+')
    #else:
    	#destination = open('%sspons_logos/%s%s'%(FILE_DIR, %event.id), 'wb+')
    #for chunk in file_obj.chunks():
        #destination.write(chunk)
    #destination.close()

#def edit_event(request):
    #if request.method == 'POST':
        #form = EventForm(request.POST, request.FILES)
        #if form.is_valid():
            #handle_uploaded_logo(request.FILES['logo'], request.POST['id'], 'logo')
            #form.save()
            #return HttpResponseRedirect('%sevents/dashboard/'%settings.SITE_URL)
    #else:
        #form = EventForm()
    #return render_to_response('edit_event.html', {'form': form}, locals(), context_instance=global_context(request))




