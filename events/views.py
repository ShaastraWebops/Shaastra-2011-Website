from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
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

FILE_DIR = settings.MEDIA_ROOT + 'main/files/'

#Will change the model after this plan is confirmed
def fileuploadhandler(f, eventname, tabid, file_title):
    savelocation = settings.MEDIA_ROOT + 'main/events/' + camelize(eventname) + '/files/' + camelize(f.name)
    destination = open( savelocation , 'wb+')
    #destination.write(f.read())
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    tab_of_file = models.QuickTabs.objects.get(id = tabid)
    tabfileobject = models.TabFiles ( Tab = tab_of_file,url = settings.MEDIA_URL + 'main/events/' + camelize(eventname) + '/files/' + camelize(f.name), title =  file_title)
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
                return HttpResponseRedirect ("%sevents/dashboard/" % settings.SITE_URL)
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
    urlname=decamelize(event_name)
    tab_list=models.QuickTabs.objects.filter(event__name = urlname).order_by('pref')
    if tab_list.count():
        for t in tab_list:
            t.file_list = models.TabFiles.objects.filter(Tab = t)
    #So each object in tab_list will have a file_list which is a list of urls to be displayed for the correspdong tab    
        display_edit = False
        if request.method=='POST': 
            user=request.user
            userprof=user.get_profile()
            event = userprof.coord_event            #this event variable is used in the template
            if userprof.is_coord == True and event.name == event_name:
                display_edit=True  
        return render_to_response('event/QuickTabs.html', locals(), context_instance= global_context(request))
    else:
        raise Http404    

@needs_authentication    
@coords_only
def dashboard(request):
    userprof = request.user.get_profile()
    if userprof.is_coord:
        event_name = userprof.coord_event.name
        tab_list = models.QuickTabs.objects.filter(event__name = event_name).order_by('pref')  
        questions_added = False
        for t in tab_list:
            t.file_list = models.TabFiles.objects.filter(Tab = t)
            if(t.question_tab):
                questions_added = True
                ques_list = models.Question.objects.filter(event__name = event_name).order_by('Q_Number')
        print questions_added
        return render_to_response('event/dashboard.html', locals(), context_instance= global_context(request))
    else:
        raise Http404        


@needs_authentication    
@coords_only
def Question_Tab(request):
    userprof = request.user.get_profile()
    if userprof.is_coord:
        event_name = userprof.coord_event.name
        ques_list = models.Question.objects.filter(event__name = event_name).order_by('Q_Number')  
        
        #for t in tab_list:
            #t.file_list = models.TabFiles.objects.filter(Tab = t)
            #if(t.question_tab):
                #questions_added = True
        print questions_added
        return render_to_response('event/Question.html', locals(), context_instance= global_context(request))
    else:
        raise Http404        





@needs_authentication    
@coords_only
def edit_tab_content(request):
    tab_to_edit=models.QuickTabs.objects.get(id=request.session["tab_id"])            
    if(tab_to_edit.question_tab):
        return edit_questions_tab_content(request)
    print "don't come here"
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
                tab_to_edit.pref = form.cleaned_data['tab_pref']
                tab_to_edit.save()
                file_list = models.TabFiles.objects.filter(Tab = tab_to_edit)
                #if request.FILES:
                    #userprof=request.user.get_profile()
                    #event_name = userprof.coord_event.name
                    #fileuploadhandler(request.FILES['tabfile'], event_name, request.session["tab_id"], form.cleaned_data['filetitle'])
                return HttpResponseRedirect ("%sevents/dashboard/"%settings.SITE_URL)
            else: 
                is_edit_tab=True
                formadd = forms.AddFileForm()
                tab_to_edit=models.QuickTabs.objects.get(id=request.session["tab_id"])
                file_list = models.TabFiles.objects.filter(Tab = tab_to_edit)  
            return render_to_response('event/add_tab.html', locals(), context_instance= global_context(request))

    else:
        tab_to_edit = models.QuickTabs.objects.get(id=request.GET["tab_id"])
        request.session["tab_id"]=request.GET["tab_id"]
        userprof = request.user.get_profile()
        if tab_to_edit.event == userprof.coord_event and userprof.is_coord:
            form = forms.EditTabForm(initial={'title' : tab_to_edit.title , 'text' :tab_to_edit.text, 'tab_pref': tab_to_edit.pref })
            file_list = models.TabFiles.objects.filter(Tab = tab_to_edit)
            formadd = forms.AddFileForm()
            is_edit_tab=True
        #use file_list to display the urls of the files associated with each tab
            return render_to_response('event/add_tab.html', locals(), context_instance= global_context(request))
        else:
            raise Http404



@needs_authentication    
@coords_only
def edit_questions(request):  
    print "hello"
    if request.method=='POST':      
            data=request.POST.copy()
            #try:
               # form = forms.EditTabForm(data,request.FILES)
            #except :  
            form = forms.EditQuestionForm(data)
            
            if form.is_valid():
                ques_to_edit=models.Question.objects.get(id=request.session["ques_id"])            
                ques_to_edit.title= form.cleaned_data['title']
                #tab_to_edit.text = form.cleaned_data['text']
                ques_to_edit.Q_Number = form.cleaned_data['Q_Number']
                ques_to_edit.save()
                #file_list = models.TabFiles.objects.filter(Tab = tab_to_edit)
                return HttpResponseRedirect ("%sevents/dashboard/"%settings.SITE_URL)
            else: 
                is_edit_tab=True
                #formadd = forms.AddFileForm()
                ques_to_edit=models.Question.objects.get(id=request.session["ques_id"])
                #file_list = models.TabFiles.objects.filter(Tab = tab_to_edit)  
            return render_to_response('event/add_questions.html', locals(), context_instance= global_context(request))

    else:
        ques_to_edit = models.Question.objects.get(id=request.GET["ques_id"])
        request.session["ques_id"]=request.GET["ques_id"]
        userprof = request.user.get_profile()
        if ques_to_edit.event == userprof.coord_event and userprof.is_coord:
            form = forms.EditQuestionForm(initial={'title' : ques_to_edit.title ,'Q_Number': ques_to_edit.Q_Number })
            #file_list = models.TabFiles.objects.filter(Tab = tab_to_edit)
            #formadd = forms.AddFileForm()
            is_edit_tab=True
            return render_to_response('event/add_questions.html', locals(), context_instance= global_context(request))
        else:
            raise Http404
        
@needs_authentication
@coords_only
def add_file(request):
    if request.method=='POST':      
            data=request.POST.copy()
            try:
                formadd = forms.AddFileForm(data,request.FILES)
            except :  
                formadd = forms.AddFileForm(data)
            
            if formadd.is_valid():
                tab_to_edit=models.QuickTabs.objects.get(id=request.session["tab_id"])
                file_list = models.TabFiles.objects.filter(Tab = tab_to_edit)
                form = forms.EditTabForm(initial={'title' : tab_to_edit.title , 'text' :tab_to_edit.text, 'tab_pref': tab_to_edit.pref })
                if request.FILES:
                    userprof=request.user.get_profile()
                    event_name = userprof.coord_event.name
                    fileuploadhandler(request.FILES['tabfile'], event_name, request.session["tab_id"], formadd.cleaned_data['filetitle'])
                #return HttpResponseRedirect ("%sevents/dashboard/edit_tab/?tab_id=%d"%settings.SITE_URL%drequest.session["tab_id"])
                is_edit_tab=True  
                return render_to_response('event/add_tab.html', locals(), context_instance= global_context(request))
    #else:
            tab_to_edit=models.QuickTabs.objects.get(id=request.session["tab_id"])
            file_list = models.TabFiles.objects.filter(Tab = tab_to_edit)
            form = forms.EditTabForm(initial={'title' : tab_to_edit.title , 'text' :tab_to_edit.text, 'tab_pref': tab_to_edit.pref }) 
            is_edit_tab=True  
            #formadd = forms.AddFileForm()
            return render_to_response('event/add_tab.html', locals(), context_instance= global_context(request))


@needs_authentication         
@coords_only
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
            newtab=models.QuickTabs(title=form.cleaned_data['title'], text=form.cleaned_data['text'], pref=form.cleaned_data['tab_pref'],event= userprof.coord_event , question_tab = False)
            newtab.save()
            #if request.FILES:     
                #fileuploadhandler(request.FILES["tabfile"], event_name, newtab.id, form.cleaned_data['filetitle'])
            return HttpResponseRedirect ("%sevents/dashboard/"%settings.SITE_URL)
    else:
        form = forms.EditTabForm()
        is_edit_tab=False
    return render_to_response('event/add_tab.html', locals(), context_instance= global_context(request))    


@needs_authentication         
@coords_only
def add_questions_tab(request):
    userprof=request.user.get_profile()
    event_name = userprof.coord_event.name
    if request.method=='POST':
        data=request.POST.copy()
        if request.FILES:
            form = forms.EditQuestionsTabForm(data,request.FILES)
        else :
            form = forms.EditQuestionsTabForm(data)    
        if form.is_valid():
            newtab=models.QuickTabs(title=form.cleaned_data['title'], text="" , pref=form.cleaned_data['tab_pref'],event= userprof.coord_event, question_tab= True)
            print "blah"
            newtab.save()
            return HttpResponseRedirect ("%sevents/dashboard/"%settings.SITE_URL)
    else:
        form = forms.EditTabForm()
        is_edit_tab=False
    return render_to_response('event/add_tab.html', locals(), context_instance= global_context(request))    

@needs_authentication
@coords_only
def add_question(request):
    userprof=request.user.get_profile()
    event_name = userprof.coord_event.name
    
    if request.method=='POST':
        data=request.POST.copy()
        #request.session["tab_id"]=request.GET["tab_id"]    
        #if request.FILES:
            #form = forms.EditQuestionForm(data,request.FILES)
        #else :
        form = forms.EditQuestionForm(data)    
        if form.is_valid():
           newquestion=models.Question(Q_Number=form.cleaned_data['Q_Number'], title=form.cleaned_data['title'],event= userprof.coord_event)
           newquestion.save()
            #if request.FILES:     
                #fileuploadhandler(request.FILES["tabfile"], event_name, newtab.id, form.cleaned_data['filetitle'])
           return HttpResponseRedirect ("%sevents/dashboard/"%settings.SITE_URL)
    else:
        form = forms.EditQuestionForm()
        is_edit_tab=False
    return render_to_response('event/add_tab.html', locals(), context_instance= global_context(request))    
 


@needs_authentication            
@coords_only
def remove_quick_tab(request):
    tabs_id=request.POST["tab_id"]
    tab_to_delete = models.QuickTabs.objects.get(id = tabs_id)
    tab_files_list = models.TabFiles.objects.filter(Tab = tab_to_delete)
    for tab_file in tab_files_list:
        tab_file.delete()
    tab_to_delete.delete()
    return HttpResponseRedirect('%sevents/dashboard/'%settings.SITE_URL)


@needs_authentication            
@coords_only
def remove_question(request):
    ques_id=request.POST["ques_id"]
    ques_to_delete = models.Question.objects.get(id = ques_id)
    #ques_list = models.Question.objects.filter(Tab = tab_to_delete)
    #for tab_file in tab_files_list:
        #tab_file.delete()
    ques_to_delete.delete()
    return HttpResponseRedirect('%sevents/dashboard/'%settings.SITE_URL)




@needs_authentication
@coords_only
def remove_file(request):
    if request.method == 'POST':
        tabfile_id = request.POST['tabfile_id']
        file_to_remove = models.TabFiles.objects.get(id = tabfile_id)
        file_to_remove.delete()
    #return HttpResponseRedirect("%sevents/dashboard/"%settings.SITE_URL)
    tab_to_edit=models.QuickTabs.objects.get(id=request.session["tab_id"])
    file_list = models.TabFiles.objects.filter(Tab = tab_to_edit)
    form = forms.EditTabForm(initial={'title' : tab_to_edit.title , 'text' :tab_to_edit.text, 'tab_pref': tab_to_edit.pref }) 
    formadd = forms.AddFileForm()
    is_edit_tab=True  
    return render_to_response('event/add_tab.html', locals(), context_instance= global_context(request))    

def logout(request):
    if request.user.is_authenticated():
        auth.logout (request)
        return render_to_response('event/logout.html', locals(), context_instance= global_context(request))        
    return HttpResponseRedirect('%sevents/login/'%settings.SITE_URL)        

@needs_authentication
@coords_only
def edit_event(request):
    user = request.user
    userprof = user.get_profile()
    event = userprof.coord_event
    if request.method == 'POST':
        try:
            form = forms.EventForm(request.POST, request.FILES, instance=event)
        except:
            form = forms.EventForm(request.POST, instance=event)
        if form.is_valid():
            print 'form is valid'
            form.save()
            return HttpResponseRedirect('%sevents/dashboard/'%settings.SITE_URL)
    else:
        form = forms.EventForm(instance = event)
    return render_to_response('event/edit_event.html', locals(), context_instance=global_context(request))

@needs_authentication
def register(request):
    user = request.uesr
    userprof = user.get_profile()
    event_id = request.GET['event_id']
    event = Event.objects.get(id = event_id)
    userprof.registered.add(event)
    return HttpResponseRedirect('%myshaastra/'%settings.SITE_URL)

@needs_authentication
@coords_only
def show_registered_users(request):
    if request.method == 'GET':
        event_id = request.GET['event_id']
        event = Event.objects.get(id = event_id)
        users_list = event.userprofile_set
        return render_to_response('show_registered_users.html', locals(), context_instance = global_context(request))
    else:
        return HttpResponseRedirect('%sevents/dashboard' % settings.SITE_URL)

