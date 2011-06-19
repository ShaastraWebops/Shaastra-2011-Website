from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.contrib import auth
from django.template.loader import get_template
from django.template.context import Context, RequestContext
from django import forms
from main_test.misc.util import *               
from main_test.settings import *
from main_test.submissions import *
#from submissions import *
import models,forms
import sha, random
import datetime

import os

#Fileupload is not done perfectly. 
#Desired - Once a file is uploaded page should be refreshed and the uploaded file should be visible as a url link below the textarea

FILE_DIR = settings.MEDIA_ROOT + 'files/'

#Will change the model after this plan is confirmed
def fileuploadhandler(f, eventname, tabid, file_title):
    savelocation = settings.MEDIA_ROOT + 'events/' + camelize(eventname) + '/files/' + camelize(f.name)
    destination = open( savelocation , 'wb+')
    #destination.write(f.read())
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    tab_of_file = models.QuickTabs.objects.get(id = tabid)
    tabfileobject = models.TabFiles ( Tab = tab_of_file,url = settings.MEDIA_URL + 'events/' + camelize(eventname) + '/files/' + camelize(f.name), title =  file_title)
    tabfileobject.save()


    
#Handler for displaying /2011/event/eventname page 
def show_quick_tab(request,event_name=None):
    urlname=decamelize(event_name)
    tab_list=models.QuickTabs.objects.filter(event__name = urlname).order_by('pref')
    event=models.Event.objects.get(name = urlname)
    ques_list= list()
    if tab_list.count():
        for t in tab_list:
            t.file_list = models.TabFiles.objects.filter(Tab = t)
            if(t.question_tab):
                    questions_added = True
                    ques_list = models.Question.objects.filter(event__name = event_name).order_by('Q_Number')
    #So each object in tab_list will have a file_list which is a list of urls to be displayed for the correspdong tab    
        display_edit = False
        if request.method=='POST': 
            user=request.user
            userprof=user.get_profile()
            event = userprof.coord_event            #this event variable is used in the template
            if userprof.is_coord == True and event.name == event_name:
                display_edit=True  
        options_list = []
        for ques in ques_list:
            temp = models.MCQ_option.objects.filter(question=ques).order_by('option')
            for temps in temp:
                options_list.append(temps)
        event_name = event.display_name
        #return render_to_response('event/QuickTabs.html', locals(), context_instance= global_context(request))
        return render_to_response('event/events_quick_tab.html', locals(), context_instance= global_context(request))
    else:
        raise Http404    

@needs_authentication    
@coords_only
def dashboard(request):
    userprof = request.user.get_profile()
    event = userprof.coord_event
    if userprof.is_coord:
        event_name = userprof.coord_event.name
        tab_list = models.QuickTabs.objects.filter(event__name = event_name).order_by('pref')  
        if(event.questions):
            questions_added = False
        else:
            questions_added = True
        for t in tab_list:
            t.file_list = models.TabFiles.objects.filter(Tab = t)
            if(t.question_tab):
                questions_added = True
                ques_list = models.Question.objects.filter(event__name = event_name).order_by('Q_Number')
                options_list = []
                for ques in ques_list:
                    temp = models.MCQ_option.objects.filter(question=ques).order_by('option')
                    for temps in temp:
                        options_list.append(temps)
                is_coord=userprof.is_coord
        event_name = userprof.coord_event.display_name
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
    tab_to_edit=models.QuickTabs.objects.get(id=request.GET['tab_id'])            
    if request.method=='POST':      
            data=request.POST.copy()
            try:
                if(tab_to_edit.question_tab):
                    forms.EditQuestionsTabForm(data,request.FILES)
                else:
                    form = forms.EditTabForm(data,request.FILES)
            except: 
                if(tab_to_edit.question_tab):
                    forms.EditQuestionsTabForm(data)
                else:
                    form = forms.EditTabForm(data)
            if form.is_valid():
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
                is_question=False
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
            is_question=False
        #use file_list to display the urls of the files associated with each tab
            return render_to_response('event/add_tab.html', locals(), context_instance= global_context(request))
        else:
            raise Http404



@needs_authentication    
@coords_only
def edit_questions(request):  
    if request.method=='POST':      
            data=request.POST.copy()  
            form = forms.EditQuestionForm(data)
            if form.is_valid():
                print request.session["ques_id"]
                ques_to_edit=models.Question.objects.get(id=request.session["ques_id"])            
                ques_to_edit.title= form.cleaned_data['title']
                ques_to_edit.Q_Number = form.cleaned_data['Q_Number']
                ques_to_edit.question_type = form.cleaned_data['question_type']
                ques_to_edit.save()
                return HttpResponseRedirect ("%sevents/dashboard/"%settings.SITE_URL)
            else: 
                is_edit_tab=True
                is_question=True
                ques_to_edit=models.Question.objects.get(id=request.session["ques_id"])  
            return render_to_response('event/add_questions.html', locals(), context_instance= global_context(request))

    else:
        ques_to_edit = models.Question.objects.get(id=request.GET["ques_id"])
        request.session["ques_id"]=request.GET["ques_id"]
        userprof = request.user.get_profile()
        if ques_to_edit.event == userprof.coord_event and userprof.is_coord:
            form = forms.EditQuestionForm(initial={'title' : ques_to_edit.title ,'Q_Number': ques_to_edit.Q_Number , 'question_type':ques_to_edit.question_type})
            #formadd = forms.AddFileForm()
            is_edit_tab=True
            is_question=True
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
                is_question=False  
                return render_to_response('event/add_tab.html', locals(), context_instance= global_context(request))
    #else:
            tab_to_edit=models.QuickTabs.objects.get(id=request.session["tab_id"])
            file_list = models.TabFiles.objects.filter(Tab = tab_to_edit)
            form = forms.EditTabForm(initial={'title' : tab_to_edit.title , 'text' :tab_to_edit.text, 'tab_pref': tab_to_edit.pref }) 
            is_edit_tab=True
            is_question=False  
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
        is_question=False 
    return render_to_response('event/add_tab.html', locals(), context_instance= global_context(request))    
    
@needs_authentication            
@coords_only
def add_choices(request):
    userprof=request.user.get_profile()
    event_name = userprof.coord_event.name
    if request.method=='POST':
        data=request.POST.copy()
        form = forms.AddContactForm(data)    
        if form.is_valid():
            print request.GET["ques_to_add_choices_id"]
            ques_to_edit=models.Question.objects.get(id=request.GET["ques_to_add_choices_id"])
            newtab= models.MCQ_option(option=form.cleaned_data['option'], text=form.cleaned_data['text'], question = ques_to_edit)
            newtab.save()
            return HttpResponseRedirect ("%sevents/dashboard/"%settings.SITE_URL)
    else:
        form = forms.AddContactForm()
        is_edit_tab=False
        is_question=False 
    return render_to_response('event/add_choices.html', locals(), context_instance= global_context(request))

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
        is_question=True
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
           newquestion=models.Question(Q_Number=form.cleaned_data['Q_Number'], title=form.cleaned_data['title'],event= userprof.coord_event, question_type=form.cleaned_data['question_type'])
           newquestion.save()
            #if request.FILES:     
                #fileuploadhandler(request.FILES["tabfile"], event_name, newtab.id, form.cleaned_data['filetitle'])
           return HttpResponseRedirect ("%sevents/dashboard/"%settings.SITE_URL)
    else:
        form = forms.EditQuestionForm()
        is_edit_tab=False
        is_question=True
    return render_to_response('event/add_questions.html', locals(), context_instance= global_context(request))    
 


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
def delete_option(request):
    option_id=request.POST["option_id"]
    print option_id
    option_to_delete = models.MCQ_option.objects.get(id = option_id)
    print option_to_delete.text
    option_to_delete.delete()
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
    event = models.Event.objects.get(id = event_id)
    userprof.registered.add(event)
    return HttpResponseRedirect('%myshaastra/'%settings.SITE_URL)

@needs_authentication
@coords_only
def show_registered_users(request):
    if request.method == 'GET':
        event_id = request.GET['event_id']
        event = models.Event.objects.get(id = event_id)
        users_list = event.userprofile_set
        return render_to_response('show_registered_users.html', locals(), context_instance = global_context(request))
    else:
        return HttpResponseRedirect('%sevents/dashboard' % settings.SITE_URL)

def show_event_categories(request):

    menu_list = models.Menu.objects.all()
    categories = menu_list.filter(parent_menu = None)
    for category in categories:
        category.events = []
        #menu_set is the reverse foreign key manager for the Menu object
        event_menu_list = category.menu_set.all()
        for event_menu in event_menu_list:
            event = event_menu.event
            event_name = camelize(event.name)
            event.image_src = SITE_URL + "events/images/" + event_name + "/"
            category.events.append(event)
    return render_to_response('show_event_categories.html', locals(), context_instance = global_context(request))


'''
def show_menu_items(request):
    if request.method == 'GET':
        menu_id = request.GET['menu_id']
        menu = models.Menu.objects.get(id = menu_id)
        #Now to get all the children of this menu
        menu_list = menu.menu_set.all()
        event_list = []
        for menu_item in menu_list:
            event_list.append(menu_item.event)
        return render_to_response('event/show_menu_items.html', locals(), context_instance = global_context(request))
    else:
        return HttpResponseRedirect('%sevents/' % settings.SITE_URL)
'''

def event_image(request, event_name=None):
    image_src = MEDIA_URL + "events/" + event_name + "/images/" + event_name + ".jpg"
    return render_to_response('event_image.html', locals(), context_instance = global_context(request))

