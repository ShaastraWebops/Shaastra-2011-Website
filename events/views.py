from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.contrib import auth
from django.template.loader import get_template
from django.template.context import Context, RequestContext
from django import forms
from main_test.misc.util import *               
from main_test.settings import *
from main_test.users.models import Team
from main_test.submissions.models import *
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
    savelocation = settings.MEDIA_ROOT + settings.EVENTS_PATH + camelize(eventname) + '/files/' + camelize(f.name)
    destination = open( savelocation , 'wb+')
    #destination.write(f.read())
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    tab_of_file = models.QuickTabs.objects.get(id = tabid)
    tabfileobject = models.TabFiles ( Tab = tab_of_file,url = settings.MEDIA_URL + settings.EVENTS_PATH + camelize(eventname) + '/files/' + camelize(f.name), title =  file_title)
    tabfileobject.save()


    

def userportal_submissions(request,questionList,event):
    nQuestions = len( questionList )
    questionId = []
    questionAnswer = []
    questionType = []
    print "doing submissions.."
    for i in range(nQuestions):
        try:
            questionId.append(request.POST['question'+str(i+1)])
            questionType.append(request.POST['type'+str(i+1)])
        except: 
            return
            
    
    #TODO: change this according to individiual/team. It's only team for now.
    # Do whatever magic you need to do and give me a team instance. Thanks. :)
    try:
        team = Team.objects.get(members__pk = request.user.id, event = event)
    except Team.DoesNotExist:
        return True
    submission = TeamSubmission( event = event , team = team )
    submission.save()
    
    for i in range( nQuestions ):
        questionObject = models.Question.objects.get( id = questionId[i] )
        if( questionType[i] == "NORMAL"):
            normalAns = Answer_Text( question = questionObject , submission = submission , text = request.POST['answer'+str(i+1)]) 
            normalAns.save() 
            print "saved text answer"
        elif ( questionType[i] == "FILE" ):
            fileAns = Answer_file( question = questionObject , submission = submission , File = request.FILES['answer'+str(i+1)])
            print "saved file answer....."
            fileAns.save()
        else:
            mcqAns = Answer_MCQ( question = questionObject , submission = submission , choice = models.MCQ_option.objects.get( id = int(request.POST['answer'+str(i+1)]) ))
            print "saved MCQ answer"
            mcqAns.save()
            
        
    answers = []
    
    print "awesomeSauce!"

#Handler for displaying /2011/event/eventname page 
def show_quick_tab(request,event_name=None):
    urlname=decamelize(event_name)
    tab_list=models.QuickTabs.objects.filter(event__name = urlname).order_by('pref')
    try:
        category = models.Menu.objects.filter(parent_menu = None).get(text = urlname) 
        category.events_list = []
        event_menu_list = category.menu_set.select_related('event').all()
        for event_menu in event_menu_list:
            event = event_menu.event
            category.events_list.append(event)
        return render_to_response('event/show_menu_items.html', locals(), context_instance = global_context(request))
    except models.Menu.DoesNotExist:
        pass
    try:
        event=models.Event.objects.get(name = urlname)
    except models.Event.DoesNotExist:
        raise Http404
    cat_name = ""
    cam_cat_name = ""
    if event.name  == "testevent":
        pass
    else:
        cat_name = str(models.Menu.objects.get(event = event).parent_menu)
        cam_cat_name = camelize(cat_name)
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
            try:
                user=request.user
                userprof=user.get_profile()
                event = userprof.coord_event            #this event variable is used in the template
            except:
                pass
            else:
                if userprof.is_coord == True and event.name == event_name:
                    display_edit=True
            val = userportal_submissions(request,ques_list,event)
            if val:
                return HttpResponseRedirect('%smyshaastra/teams/create/' % settings.SITE_URL)
        options_list = []
        for ques in ques_list:
            temp = models.MCQ_option.objects.filter(question=ques).order_by('option')
            for temps in temp:
                options_list.append(temps)
        event_name = None
        event = None
        user_has_registered = False
        show_register = False
        try:
            event = models.Event.objects.get(name = urlname)
            event_name = event.display_name
            if event.registrable:
                show_register = True
            try:
                request.user.get_profile().registered.get(pk = event.id)
                user_has_registered = True
            except:
                pass
        except:
            raise Http404
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




def sitemap(request):
    urls = ['/home/',]
    querySet = models.Event.objects.all()
    for query in querySet:
        urls.append(query.url)
    return render_to_response('sitemap.xml', locals(), context_instance= global_context(request))


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
    
@coords_only    
def add_event_update(request):
    if request.method =='POST':
        data=request.POST.copy()
        form=forms.EventUpdateForm(data)
        if form.is_valid():
            neweventupdate=models.Update(event = request.user.get_profile().coord_event , content_formatted = form.cleaned_data['UpdateContent'])
            neweventupdate.save()
        return HttpResponseRedirect('%sevents/dashboard/updates/'%settings.SITE_URL)    
    else:
        form=forms.EventUpdateForm()
    return render_to_response('event/add_update.html', locals(), context_instance=global_context(request))
        
@coords_only 
def updates_page(request):
    
    updates_list=models.Update.objects.filter(event=request.user.get_profile().coord_event)
    return render_to_response('event/updates_page.html', locals(), context_instance=global_context(request))
    
            
             
@needs_authentication
def register(request):
    user = request.user
    userprof = user.get_profile()
    if request.method == 'GET':
        event_id = request.GET['event_id']
    else:
        raise Http404
    event = models.Event.objects.get(id = event_id)
    userprof.registered.add(event)
    return HttpResponseRedirect(event.url)

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
    return render_to_response('event/show_event_categories.html', locals(), context_instance = global_context(request))


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
    image_src = "" #Need a default image
    if event_name is not None:
        event = models.Event.objects.get(name = decamelize(event_name))
        image_src = event.menu_image.url
    return render_to_response('event/event_image.html', locals(), context_instance = global_context(request))

'''
def search(request):
    if request.method == "GET":
        search_string = request.GET["search_string"]
        s, junk = search_string.split(' ', 1)
        result_urls = []
        result = models.Event.objects.filter(display_name__icontains = s)
        if result.
'''

@needs_authentication
@coords_only
def cores_dashboard(request):
    if request.user.username == 'cores':
        if request.method == 'GET' and 'event_id' in request.GET:
            event_id = request.GET['event_id']
            try:
                event = models.Event.objects.get(id = event_id)
                userprofile = request.user.get_profile()
                userprofile.coord_event = event
                userprofile.save()
                return HttpResponseRedirect("%sevents/dashboard" % settings.SITE_URL)
            except models.Event.DoesNotExist:
                raise Http404
        else:
            events = models.Event.objects.all()
            return render_to_response('event/cores_dashboard.html', locals(), context_instance = global_context(request))
    return HttpResponseRedirect("%sevents/dashboard" % settings.SITE_URL)

@needs_authentication
@cores_only
def UpdateSpons(request):
    
    if request.method=='POST':
        data=request.POST.copy()
        form = forms.UpdateSpons(data)
        if form.is_valid():
               
            newtab=models.UpdateSpons(text=form.cleaned_data['text'])
            newtab.save()
            
        return HttpResponseRedirect("%shome" % settings.SITE_URL)
    else:
        form = forms.UpdateSpons()
    return render_to_response('update_spons.html', locals(), context_instance= global_context(request))      
    
#having a common render_static function

def render_static(request,static_name):

      
    if static_name=="policy":
        return render_to_response('policy.html', locals(), context_instance = global_context(request))    
    if static_name=="hospitality":
        return render_to_response('hospi.html', locals(), context_instance = global_context(request))    
    if static_name=="sponsorship":
        return render_to_response('spons.html', locals(), context_instance = global_context(request))    
    if static_name=="credits":
        return render_to_response('credits.html', locals(), context_instance = global_context(request))    
    if static_name=="contact":
        return render_to_response('contacts.html', locals(), context_instance = global_context(request)) 
    if static_name=="Developers":
        return render_to_response('webteam.html', locals(), context_instance = global_context(request))
    
    raise Http404
        
""" 
def render_policy(request):
    return render_to_response('policy.html', locals(), context_instance = global_context(request))
def render_hospitality(request):
    return render_to_response('hospi.html', locals(), context_instance = global_context(request))
def render_sponsorship(request):
    return render_to_response('spons.html', locals(), context_instance = global_context(request))
def render_credits(request):
    return render_to_response('credits.html', locals(), context_instance = global_context(request))
def render_contact(request):
    return render_to_response('contacts.html', locals(), context_instance = global_context(request))    
"""    
