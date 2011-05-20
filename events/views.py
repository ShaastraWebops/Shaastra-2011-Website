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
#Fileupload is not done perfectly. 
#Desired - Once a file is uploaded page should be refreshed and the uploaded file should be visible as a url link below the textarea

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
#Handler for displaying /2011/event/eventname page 
def show_quick_tab(request,event_name=None):
    tab_list=models.QuickTab.objects.filter(event.name = event_name)
    for t in tab_list
        self.file_list=unicode(models.TabFile.objects.filter(Tab = self ))
    #So each object in tab_list will have a file_list which is a list of urls to be displayed for the correspdong tab    
    display_edit = False
    if request.method=='POST': 
        user=request.user
        userprof=user.get_profile()
        if userprof.is_coord == True and userprof.coord_event.name == event_name
            display_edit=True  
    return render_to_response('events/QuickTabs.html', locals(), context_instance= global_context(request)) 
    
def dashboard(request):
    userprof=request.user.get_profile()
    event_name = userprof.coord_event.self()
    if request.method=='POST':
        user = request.user
        userprof = user.get_profile()
        tab_list = models.QuickTab.objects.filter(event = userprof.coord_event)
        
    return render_to_response('events/dashboard.html', locals(), context_instance= global_context(request))    

@needs_authentication
@coords_only    
def edit_tab_content(request):
    userprof=request.user.get_profile()
    event_name = userprof.coord_event.self()
    #just a check if the coord is viewing the right page...
    if request.method=='POST': 
        user=request.user
        userprof=user.get_profile()
        tabs_id=request.POST["tab_id"]
        tab_to_edit=models.QuickTabs.objects.filter(id = tabs_id)
        data=request.POST.copy()
        filedata=request.FILES.copy()
        tab_file_list='%sTabFile/%s'%(FILE_DIR,tab_to_edit.files)
        fileurllist=[]
        #Display the tab_file_list as a list in after text area
        form = forms.EditTabForm(data,filedata,initial={'title': tab_to_edit.title,'text': tab_to_edit.text})
        if form.cleaned_data['title']=="":
            form = forms.EditTabForm()
            return render_to_response('events/edit_tab.html', locals(), context_instance= global_context(request))
        if form.is_valid():
            tab_to_edit.title= form.cleaned_data['title']
            tab_to_edit.text = form.cleaned_data['text']
            filetitle = form.cleaned_data['filetitle']
            tab_to_edit.save()
            filetosave=request.FILES['tabfile']
            tabfile=TabFile(File=filetosave,Tab=tab_to_edit,filename=filetosave['filename'],title=filetitle)
            tabfile.save()
            fileurllist=unicode(models.TabFile.objects.filter(Tab = tab_to_edit))            
    #use fileurllist to display the urls of the files associated with each tab
    else:
        form = forms.EditTabForm()
    return render_to_response('events/edit_tab.html', locals(), context_instance= global_context(request))
        
def add_quick_tab(request):
    userprof=request.user.get_profile()
    event_name = userprof.coord_event.self()
    if request.method=='POST'
        newtab=QuickTab(title='', text='', pref_no=0 , event= userprof.coord_event ,Files = '')
        data=request.POST.copy()
        filedata = request.FILES.copy()
        form = forms.EditTabForm(data,filedata)
        fileurllist=[]
        if form.cleaned_data['title']=="":
            form = forms.EditTabForm()
            return render_to_response('events/edit_tab.html', locals(), context_instance= global_context(request))
        else if form.is_valid():
            newtab.title= form.cleaned_data['title']
            newtab.text = form.cleaned_data['text']
            filetitle = form.cleaned_data['filetitle']
            newtab.pref=form.cleaned_data['tab_pref']
            newtab.save()
            filetosave=request.FILES['tabfile']
            tabfile=TabFile(File=filetosave,Tab=newtab,filename=filetosave['filename'],title=filetitle)
            tabfile.save()
    else:
        form = forms.EditTabForm()
    return render_to_response('event/add_tab.html', locals(), context_instance= global_context(request))    
        
            
def remove_quick_tab(request):
    userprof=request.user.get_profile()
    event_name = userprof.coord_event.self()
    if request.method=='POST'
        tabs_id=request.session["tab_id"]
        tab_to_delete=models.QuickTab.objects.filter(id=tabs_id)
        tab_to_delete.delete()
    return HttpResponseRedirect('/events/edit/')    
            




