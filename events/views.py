from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.template.loader import get_template
from django.template.context import Context, RequestContext
from django import forms

from main_test.misc.util import *               #Importing everything - just in case
from main_test.settings import *
import models,forms

import datetime

import os
#Fileupload is not done perfectly. 
#Desired - Once a file is uploaded page should be refreshed and the uploaded file should be visible as a url link below the textarea

#We can check if coords are logged in using the request.session['logged_in'] variable and then allow them to edit the corresponding event page after verifying this.
IMAGE_DIR = '2011/media/main/images/'
FILE_DIR = '2011/media/main/files/'

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
                url="%sevents/login"%settings.SITE_URL
                #This URL can be changed as required later
                response= HttpResponseRedirect (url)
                return response
        else:                       
            invalid_login = session_get(request, "invalid_login")
            form = forms.CoordsLoginForm () 
    return render_to_response('event/login.html', locals(), context_instance= global_context(request))
    #This URL can be changed as required later
                   
#I m _not_ writing templates write now. Just creating empty html files.
#Handler for displaying /2011/event/eventname page 
def show_quick_tab(request,event_name=None):
    tab_list=models.QuickTabs.objects.filter(event__name = event_name)
    #for t in tab_list:
    #    self.file_list=unicode(models.TabFile.objects.filter(Tab = self ))
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
    #if request.method=='POST':
    
    userprof=request.user.get_profile()
    event_name = userprof.coord_event.name
    tab_list = models.QuickTabs.objects.filter(event__name = event_name)  
    return render_to_response('event/dashboard.html', locals(), context_instance= global_context(request))    

   
def edit_tab_content(request):
    userprof=request.user.get_profile()
    event_name = userprof.coord_event.name
    #just a check if the coord is viewing the right page...
    if request.method=='POST':
        try:
            tabs_id=request.POST["tab_id"]
            tab_to_edit=models.QuickTabs.objects.get(id=tabs_id)
            form = forms.EditTabForm(initial={'title' : tab_to_edit.title , 'text' :tab_to_edit.text, 'tab_pref': tab_to_edit.pref })
            request.session["tab_id"]=tabs_id
        except:        
            data=request.POST.copy()
            if request.FILES:
                tab_file_list='%sTabFile/%s'%(FILE_DIR,tab_to_edit.files)
        #Display the tab_file_list as a list in after text area
                form = forms.EditTabForm(data,request.FILES)
            else :  
                form = forms.EditTabForm(data)


            if form.is_valid():
                tab_to_edit=models.QuickTabs.objects.get(id=request.session["tab_id"])            
                tab_to_edit.title= form.cleaned_data['title']
                tab_to_edit.text = form.cleaned_data['text']
                tab_to_edit.save()
                if request.FILES:
                    filetitle = form.cleaned_data['filetitle']
                    filetosave=request.FILES['tabfile']
                    tabfile=TabFile(File=filetosave,Tab=tab_to_edit,filename=filetosave['filename'],title=filetitle)
                    tabfile.save()
                fileurllist=unicode(models.TabFile.objects.filter(Tab = tab_to_edit))
                return HttpResponseRedirect ("%sevents/dashboard/"%settings.SITE_URL)            
    #use fileurllist to display the urls of the files associated with each tab
    else:
        form = forms.EditTabForm()
    return render_to_response('event/add_tab.html', locals(), context_instance= global_context(request))
        
def add_quick_tab(request):
    userprof=request.user.get_profile()
    event_name = userprof.coord_event.name
    if request.method=='POST':
        
        data=request.POST.copy()
        if request.FILES:
            form = forms.EditTabForm(data,request.FILES)
        else :
            form = forms.EditTabForm(data)    
        fileurllist=[]
      #if form.cleaned_data['title']=="":
      #      form = forms.EditTabForm()
      #      return render_to_response('event/edit_tab.html', locals(), context_instance= global_context(request))
        if form.is_valid():
            newtab=models.QuickTabs(title=form.cleaned_data['title'], text=form.cleaned_data['text'], pref=form.cleaned_data['tab_pref'] , event= userprof.coord_event )
            newtab.save()
            if request.FILES:     
                filetitle = form.cleaned_data['filetitle']
                filetosave=request.FILES['tabfile']
                tabfile=models.TabFile(File=filetosave,Tab=newtab,filename=filetosave.name,title=filetitle) #changed filetosave['filename'] to filetosave.name
                tabfile.save()
            return HttpResponseRedirect ("%sevents/dashboard/"%settings.SITE_URL)
    else:
        form = forms.EditTabForm()
    return render_to_response('event/add_tab.html', locals(), context_instance= global_context(request))    
        
            
def remove_quick_tab(request):
    userprof=request.user.get_profile()
    event_name = userprof.coord_event.name
    tabs_id=request.POST["tab_id"]
    tab_to_delete=models.QuickTabs.objects.filter(id=tabs_id)
    tab_to_delete.delete()
    return HttpResponseRedirect('/events/dashboard/')

def logout(request):
    if request.user.is_authenticated():
        auth.logout (request)        
    return HttpResponseRedirect('/events/login/')        




