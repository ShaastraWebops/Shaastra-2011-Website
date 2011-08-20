# -*- coding: utf-8 -*-
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
    print "cumming here ..."
    nQuestions = len( questionList )
    questionId = []
    questionAnswer = []
    questionType = []
    for i in range(nQuestions):
        try:
            questionId.append(request.POST['question'+str(questionList[i].Q_Number)])
            questionType.append(request.POST['type'+str(questionList[i].Q_Number)])
        except: 
            raise
            return 
    try:
        print request.user.id, event
        team = Team.objects.get(members__pk = request.user.id, event__name = event)
        print "Yeah i go a tema"
    except Team.DoesNotExist:
        print "faaaaaaaaack!"
        return None

    e = Event.objects.get(name = event)
    if ( e.team_event ):
        submission = None
        try:
            submission = TeamSubmission.objects.get(team = team)
            for i in range( nQuestions ):
                questionObject = models.Question.objects.get( id = questionId[i] )
                if( questionType[i] == "NORMAL"):
                    try:
                        normalAns = Answer_Text.objects.get( question = questionObject , submission = submission ) 
                        normalAns.text = request.POST['answer'+str(questionList[i].Q_Number)]
                        normalAns.save() 
                    except:
                        normalAns = Answer_Text( question = questionObject , submission = submission , text = request.POST['answer'+str(questionList[i].Q_Number)]) 
                        normalAns.save()                     
                elif ( questionType[i] == "FILE" ):
                    if(  'answer'+str(questionList[i].Q_Number) in request.FILES):
                        try:
                            fileAns = Answer_file.objects.get( question = questionObject , submission = submission )
                            fileAns.File = request.FILES['answer'+str(questionList[i].Q_Number)]
                            fileAns.save()
                        except:
                            fileAns = Answer_file( question = questionObject , submission = submission , File = request.FILES['answer'+str(questionList[i].Q_Number)])
                            fileAns.save()                
                else:
                    if(  'answer'+str(questionList[i].Q_Number) in request.POST):
                        try:
                            mcqAns = Answer_MCQ.objects.get( question = questionObject , submission = submission )
                            mcqAns.choice = models.MCQ_option.objects.get( id = int(request.POST['answer'+str(questionList[i].Q_Number)]))
                            mcqAns.save()
                        except:
                            mcqAns = Answer_MCQ( question = questionObject , submission = submission , choice = models.MCQ_option.objects.get( id = int(request.POST['answer'+str(questionList[i].Q_Number)]) ))
                            mcqAns.save()                    
        except TeamSubmission.DoesNotExist:
            submission = TeamSubmission( event = e , team = team )
            submission.save()    
            for i in range( nQuestions ):
                questionObject = models.Question.objects.get( id = questionId[i] )
                if( questionType[i] == "NORMAL"):
                    if( 'answer'+str(questionList[i].Q_Number) in request.POST ):
                        normalAns = Answer_Text( question = questionObject , submission = submission , text = request.POST['answer'+str(questionList[i].Q_Number)]) 
                        normalAns.save() 
                elif ( questionType[i] == "FILE" ):
                    if( 'answer'+str(questionList[i].Q_Number) in request.POST ):
                        fileAns = Answer_file( question = questionObject , submission = submission , File = request.FILES['answer'+str(questionList[i].Q_Number)])
                        fileAns.save()
                else:
                    if( 'answer'+str(questionList[i].Q_Number)  in request.POST):
                        mcqAns = Answer_MCQ( question = questionObject , submission = submission , choice = models.MCQ_option.objects.get( id = int(request.POST['answer'+str(questionList[i].Q_Number)]) ))
                        mcqAns.save()
        return "saved"
    else:
        submission = None
        try:
            userprofile = UserProfile.objects.get( user = request.user )
            submission = IndividualSubmissions.objects.get( participant = userprofile , event = e )
            for i in range( nQuestions ):
                questionObject = models.Question.objects.get( id = questionId[i] )
                if( questionType[i] == "NORMAL"):
                    try:
                        normalAns = Answer_Text.objects.get( question = questionObject , submission = submission ) 
                        normalAns.text = request.POST['answer'+str(questionList[i].Q_Number)]
                        normalAns.save() 
                    except:
                        normalAns = Answer_Text( question = questionObject , submission = submission , text = request.POST['answer'+str(questionList[i].Q_Number)]) 
                        normalAns.save()                     
                elif ( questionType[i] == "FILE" ):
                    if(  'answer'+str(questionList[i].Q_Number) in request.FILES):
                        try:
                            fileAns = Answer_file.objects.get( question = questionObject , submission = submission )
                            fileAns.File = request.FILES['answer'+str(questionList[i].Q_Number)]
                            fileAns.save()
                        except:
                            fileAns = Answer_file( question = questionObject , submission = submission , File = request.FILES['answer'+str(questionList[i].Q_Number)])
                            fileAns.save()                
                else:
                    if(  'answer'+str(questionList[i].Q_Number) in request.POST):
                        try:
                            mcqAns = Answer_MCQ.objects.get( question = questionObject , submission = submission )
                            mcqAns.choice = models.MCQ_option.objects.get( id = int(request.POST['answer'+str(questionList[i].Q_Number)]))
                            mcqAns.save()
                        except:
                            mcqAns = Answer_MCQ( question = questionObject , submission = submission , choice = models.MCQ_option.objects.get( id = int(request.POST['answer'+str(questionList[i].Q_Number)]) ))
                            mcqAns.save()                    
        except IndividualSubmissions.DoesNotExist:
            userprofile = UserProfile.objects.get( user = request.user )
            submission = IndividualSubmissions( participant = userprofile , event  = e )
            submission.save()    
            for i in range( nQuestions ):
                questionObject = models.Question.objects.get( id = questionId[i] )
                if( questionType[i] == "NORMAL"):
                    if( 'answer'+str(questionList[i].Q_Number) in request.POST ):
                        normalAns = Answer_Text( question = questionObject , submission = submission , text = request.POST['answer'+str(questionList[i].Q_Number)]) 
                        normalAns.save() 
                elif ( questionType[i] == "FILE" ):
                    if( 'answer'+str(questionList[i].Q_Number) in request.POST ):
                        fileAns = Answer_file( question = questionObject , submission = submission , File = request.FILES['answer'+str(questionList[i].Q_Number)])
                        fileAns.save()
                else:
                    if( 'answer'+str(questionList[i].Q_Number)  in request.POST):
                        mcqAns = Answer_MCQ( question = questionObject , submission = submission , choice = models.MCQ_option.objects.get( id = int(request.POST['answer'+str(questionList[i].Q_Number)]) ))
                        mcqAns.save()
        return "saved"

#Handler for displaying /2011/event/eventname page 
def show_quick_tab(request,event_name=None):
    """"
        This is the view for the display for the event page i.e the tabs
        
        The tab_list is a list of QuickTabs objects for for event__name is the urlname
        Note that , urlname is a decamelized version of the event_name which is the event_name parameter in the URL.
        (Refer decamelize and camelize in /misc/util.py)
        
        Example:-
        www.shaastra.org/2011/main/events/Robotics/
        
        Here, "Robotics" is the event_name
        
        category is a menu object for which the menu "text" is urlname. The corresponding category image is displayed in the template
        
        If the event is registrable, a register button is displayed. Similarly, if the user is the coord for the event, a button is displayed which takes him/her to the dashboard
    """
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
	print event
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
            if(t.question_tab and event.questions):
                questions_added = True
                
                ques_list = models.Question.objects.filter(event__name = event_name).order_by('Q_Number')
    #So each object in tab_list will have a file_list which is a list of urls to be displayed for the correspdong tab    
        display_edit = False
        if request.method=='POST': 
            try:
                user=request.user
                userprof=user.get_profile()
                event = userprof.coord_event            #this event variable is used in the template
                if userprof.is_coord == True and event.name == event_name:
                    display_edit=True
            except:
                pass                

            val = None
            if ( request.user.is_authenticated()):
                val = userportal_submissions(request,ques_list,urlname)
                if val is None:
                    e = Event.objects.get(name = urlname)
                    return HttpResponseRedirect('%smyshaastra/teams/create/%s/' % [ settings.SITE_URL, e.id])
                elif val == "saved":
                    saved = True
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
        
        # get initial values for forms
        answers = []
        already_submitted = False
        zipped = [] 
        # team event => Team Submissions. 
        if( event.team_event and request.user.is_authenticated() ):
            try:
                team = Team.objects.get(members__pk = request.user.id, event = event)
                submission = TeamSubmission.objects.get( team = team , event = event )
                base_submission_id = int(submission.basesubmission_ptr_id)
                base_submission = BaseSubmission.objects.get( id = base_submission_id ) 
                for question in ques_list:
                    if( question.question_type == 'NORMAL'):
                        temp = []
                        temp.append( ques )
                        try:
                            ansText = Answer_Text.objects.get( submission = base_submission , question = question )
                            temp.append(ansText)
                        except:
                            temp.append("No normal answers")
                        zipped.append(temp)
                    elif ( question.question_type == "FILE"):
                        temp = []
                        temp.append( ques )
                        try:
                            ansFile = Answer_file.objects.get( submission = base_submission , question = question )
                            temp.append(ansFile)
                        except:
                            temp.append("No file answer")
                        zipped.append(temp)
                    elif ( question.question_type == "MCQ"):
                        temp=[]
                        temp.append(ques)
                        try:
                            ansMCQ = Answer_MCQ.objects.get( submission = base_submission , question = question )
                            temp.append(ansMCQ)
                        except:
                            temp.append("No MCQ answers")
                        option_list = []
                        for option in options_list:
                            if option.question == ques:
                                option_list.append(option)
                        zipped.append(option_list)
                        zipped.append(temp)
                already_submitted = True
            except:
                pass
        # Individual submissions
        elif ( event.team_event == False and request.user.is_authenticated() ):
            try:
                userprofile = UserProfile.objects.get( user = request.user )
                submission = IndividualSubmissions.objects.get( participant = userprofile , event = event )
                base_submission_id = int(submission.basesubmission_ptr_id)
                base_submission = BaseSubmission.objects.get( id = base_submission_id ) 
                for question in ques_list:
                    if( question.question_type == 'NORMAL'):
                        temp = []
                        temp.append( ques )
                        try:
                            ansText = Answer_Text.objects.get( submission = base_submission , question = question )
                            temp.append(ansText)
                        except:
                            temp.append("No normal answers")
                        zipped.append(temp)
                    elif ( question.question_type == "FILE"):
                        temp = []
                        temp.append( ques )
                        try:
                            ansFile = Answer_file.objects.get( submission = base_submission , question = question )
                            temp.append(ansFile)
                        except:
                            temp.append("No file answer")
                        zipped.append(temp)
                    elif ( question.question_type == "MCQ"):
                        temp=[]
                        temp.append(ques)
                        try:
                            ansMCQ = Answer_MCQ.objects.get( submission = base_submission , question = question )
                            temp.append(ansMCQ)
                        except:
                            temp.append("No MCQ answers")
                        option_list = []
                        for option in options_list:
                            if option.question == ques:
                                option_list.append(option)
                        temp.append(option_list)
                        zipped.append(temp)
                already_submitted = True
            except:
                pass
        return render_to_response('event/events_quick_tab.html', locals(), context_instance= global_context(request))
    else:
        raise Http404    

@needs_authentication    
@coords_only
def dashboard(request):
    """
        This is the view that displays the coord's dashboard. The code is similar to the show_quick_tab view
    
        This page is visible to coords only and needs authentication
    
    
    
    
    
    
    """
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
            if(t.question_tab and event.questions ):
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
                    form = forms.EditQuestionsTabForm(data,request.FILES)
                else:
                    form = forms.EditTabForm(data,request.FILES)
            except: 
                if(tab_to_edit.question_tab):
                    form = forms.EditQuestionsTabForm(data)
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
            if( tab_to_edit.question_tab ):
                form = forms.EditQuestionsTabForm(initial={'title' : tab_to_edit.title , 'tab_pref': tab_to_edit.pref })
            else:
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
    """
        This is the view for adding a new quick tab. Access is restricted to event coords.
        
        Event name is got from the userprofile object of the user .
        
        The EditTabForm is displayed without any preset data and it is saved.
        
        Files cannot be added when a tab is first added. Please ignore the form = forms.EditTabForm(data,request.FILES) part.
        
    """
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
    """
        This is the view to remove a tab. The tab id is passed as a POST parameter.
        
        The tab and the files associated with the particular tab are deleted 
        
    """    
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
    """
        This is the view to edit event details of each event. 
        
        Only the event coord can edit this page.
        
        A model form is used and the event coord can modify display_name, menu_image, sponslogo, video attributes
    """    
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
    """ 
        This is the view for registering for an event. 
        
        The event id is passed as a GET parameter and the event is added to the registered field of the userprofile model.
    """   
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
        if request.user.get_profile().is_coord != True or request.user.get_profile().coord_event != event:
            raise Http404
        users_list = event.registered_users.all()
        return render_to_response('event/show_registered_users.html', locals(), context_instance = global_context(request))
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
    """
        This is the view that displays the cores dashboard.
        
        Initially all the events are displayed. 
        
        If the core clicks on a event, the event id is passed as a GET parameter. 
        
        The coord_event field of the userprofile model is set to corresponding event and he is taken to the event dashboard.
        
        So, basically every time the core clicks on a event, he temporarily becomes a coord for the event. A nice workaround.
        
    """    
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

def UpdateSpons(request):
    if request.user.username == 'spons':    
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
    return HttpResponseRedirect("%slogin" % settings.SITE_URL) 

# having a page for the event cores to edit

@needs_authentication

def EventCoresEditPage(request):
    print "come here"
    tab_to_edit=models.EventCoresEditPage.objects.get(id=request.GET['tab_id']) 
               
    if request.method=='POST':      
            data=request.POST.copy()
            form = forms.EventCoresEditPage(data)
            
            if form.is_valid():
                tab_to_edit.text = form.cleaned_data['text']
                tab_to_edit.save()

                return HttpResponseRedirect ("%sevents/ImportantDates"%settings.SITE_URL)
            else: 
                
                tab_to_edit=models.EventCoresEditPage.objects.get(id=request.session["tab_id"])
                  
            return render_to_response('event_cores_edit.html', locals(), context_instance= global_context(request))


    else:
        
        tab_to_edit = models.EventCoresEditPage.objects.get(id=request.GET["tab_id"])
        request.session["tab_id"]=request.GET["tab_id"]
        
        if request.user.username == 'cores':
            form = forms.EventCoresEditPage(initial={'text' :tab_to_edit.text })
            return render_to_response('event_cores_edit.html', locals(), context_instance= global_context(request))
        else:
            raise Http404


def EventCoresPage(request):
    
        event_cores_content=models.EventCoresEditPage.objects.get()
        if request.user.username=="cores":
            is_core=True
        else:
            is_core=False
        return render_to_response('event_cores_page.html', locals(), context_instance= global_context(request))
    

#having a common render_static function

def render_static(request,static_name):

      
    if static_name=="policy":
        return render_to_response('policy.html', locals(), context_instance = global_context(request))    
    if static_name=="hospitality":
        return render_to_response('hospi.html', locals(), context_instance = global_context(request))    
    if static_name=="sponsorship":
        if request.user.username=="cores" or request.user.username == 'spons':
            is_core=True
        else:
            is_core=False 
        return render_to_response('spons.html', locals(), context_instance = global_context(request))    
    if static_name=="credits":
        return render_to_response('credits.html', locals(), context_instance = global_context(request))    
    if static_name=="contact":
        return render_to_response('contacts.html', locals(), context_instance = global_context(request)) 
    if static_name=="Developers":
        return render_to_response('webteam.html', locals(), context_instance = global_context(request))
    
    raise Http404

# the edit page for spons starts from here
@needs_authentication    

def edit_spons(request):
    print "come here"
    tab_to_edit=models.SponsPage.objects.get(id=request.GET['tab_id']) 
               
    if request.method=='POST':      
            data=request.POST.copy()
            form = forms.SponsPageForm(data)
            
            if form.is_valid():
                tab_to_edit.text = form.cleaned_data['text']
                tab_to_edit.save()

                return HttpResponseRedirect ("%ssponsorship"%settings.SITE_URL)
            else: 
                
                tab_to_edit=models.SponsPage.objects.get(id=request.session["tab_id"])
                  
            return render_to_response('edit_spons_page.html', locals(), context_instance= global_context(request))


    else:
        
        tab_to_edit = models.SponsPage.objects.get(id=request.GET["tab_id"])
        request.session["tab_id"]=request.GET["tab_id"]
        
        if request.user.username == 'spons':
            form = forms.SponsPageForm(initial={'text' :tab_to_edit.text })
            return render_to_response('edit_spons_page.html', locals(), context_instance= global_context(request))
        else:
            raise Http404





#edit page for the spons page ends here


        
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
