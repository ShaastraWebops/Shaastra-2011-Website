
# Create your views here.

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.template.loader import get_template
from django.template.context import Context, RequestContext
from django.utils.translation import ugettext as _
from django.core.mail import send_mail,EmailMessage,SMTPConnection
from django.contrib.sessions.models import Session

from main_test.misc.util import *
from main_test.settings import *
#from main_test.users.models import UserProfile, College
from main_test.users.models import *
import forms
import sha,random,datetime
"""
def home (request):
    redirected=session_get(request,"from_url")
    access_denied = session_get (request, "access_denied")
    logged_in = session_get (request, "logged_in")
    already_logged = session_get (request, "already_logged")
    hospi_success=session_get(request,"hospi_success")
    key = request.session.session_key
    return render_to_response('home/home.html', locals(), context_instance= global_context(request)) 

def edited (request):

    print dir(request.session)
    print request.session.keys()
    #print request.session['unb_User']
    #return render_to_response('home/home.html', locals(), context_instance= global_context(request)) 
    response = render_to_response('home/home.html', locals(), context_instance= global_context(request)) 
    return response

def registered (request):

    redirected=session_get(request,"from_url")
    access_denied = session_get (request, "access_denied")
    logged_in = session_get (request, "logged_in")
    already_logged = session_get (request, "already_logged")
    hospi_success=session_get(request,"hospi_success")
    return render_to_response('home/registered.html', locals(), context_instance= global_context(request)) 

def deadlines(request):
    return render_to_response('home/deadlines.html', locals(), context_instance= global_context(request))

@no_login
def login (request):

    redirected = request.session.get ("from_url", False)
    registered = session_get (request, "registered")
    form = forms.UserLoginForm ()

    if request.method == 'POST':
        data = request.POST.copy()
        form = forms.UserLoginForm (data)
        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data["password"])
            if user is not None and user.is_active == True:
                auth.login (request, user)
                url = session_get(request, "from_url")
                # Handle redirection
                if not url:
                	url = "%s/home/"%settings.SITE_URL
                        request.session['logged_in'] = True
                        response= HttpResponseRedirect (url)
                try:
                    response.set_cookie('logged_out', 0)
                except:
                    pass
                return response
            else:
                request.session['invalid_login'] = True
                return HttpResponseRedirect (request.path)
        else: 
            invalid_login = session_get(request, "invalid_login")
            form = forms.UserLoginForm ()
    else:
        pass
    return render_to_response('home/login.html', locals(), context_instance= global_context(request)) 

def forgot_password (request):
    if request.method == 'POST':
        data = request.POST.copy()
        form = forms.ForgotPasswordForm (data)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = models.User.objects.get(email=email)
                try:
                    userprof = UserProfile.objects.get(user=user)
                    salt = sha.new(str(random.random())).hexdigest()[:5]
                    userprof.activation_key = sha.new(salt+user.username).hexdigest()
                    userprof.save()
                    mail_template=get_template('email/forgot.html')
                    body = mail_template.render(Context({'username':user.username, 'reset_pass':userprof.activation_key}))
                    send_mail('Shaastra UserPortal Password', body, 'noreply@shaastra.org', [email,], fail_silently=False)
                    request.session['success'] = True
                except ObjectDoesNotExist:
                    request.session['invalid_email']=email
            except ObjectDoesNotExist:
                request.session['invalid_email'] = email
    else: 
        form = forms.ForgotPasswordForm ()

    success = session_get (request, "success")
    invalid_email = session_get (request, "invalid_email")
    reset = session_get(request,"reset")
    reset_fail = session_get(request,"reset_fail")
    u_name = session_get(request,"u_name")
    new_pass = session_get(request,"new_pass")

    return render_to_response('home/forgot.html', locals(), context_instance= global_context(request)) 

def reset_password(request,u_name = None,new_pass = None):

    success = session_get(request,"success")
    invalid_email = session_get(request,"invalid_email")
    reset = session_get(request,"reset")
    reset_fail = session_get(request,"reset_fail")

    if u_name is None or u_name == '':
        reset_fail = True
        return render_to_response ('home/forgot.html', locals(), context_instance = global_context(request))

    if new_pass is None or new_pass == '':
        reset_fail = True
        return render_to_response('home/forgot.html', locals(), context_instance = global_context(request))

    u_name = u_name.replace('/','')

    try:
        user = models.User.objects.get(username=u_name)
        try:
            userprofile = UserProfile.objects.get(user=user, activation_key=new_pass)
            password=auth.models.UserManager().make_random_password()
            user.set_password(password)
            user.save()
            salt = sha.new(str(random.random())).hexdigest()[:5]
            userprofile.activation_key = sha.new(salt+user.username).hexdigest()
            userprofile.save()
            request.session['password'] = password
            request.session['reset'] = True
        except ObjectDoesNotExist:
            request.session['reset_fail']=True
    except ObjectDoesNotExist:
        request.session['reset_fail'] = True

    reset = session_get(request,"reset")
    reset_fail = session_get(request,"reset_fail")
    new_pass = session_get(request,"password")

    return render_to_response('home/forgot.html', locals(), context_instance = global_context(request))

def logout (request):
    if request.user.is_authenticated():
        auth.logout (request)
        url = "%s/home/"%settings.SITE_URL
        response= HttpResponseRedirect (url)
        try:
            response.set_cookie('logged_out', 1)
        except:
            pass
        return response

    #return HttpResponseRedirect("%s/home/"%settings.SITE_URL)
    return render_to_response('home/home.html', locals(), context_instance= global_context(request)) 

def check(request):
    return HttpResponse("The Site Url Is %s" %SITE_URL)




# just copied the user registration
# i dont think much of changes required 

"""
def user_registration(request):
    colls = models.College.objects.all()
    if request.method=='POST':
	data = request.POST.copy()
        form = forms.AddUserForm (data)
        
        if form.is_valid():
            if form.cleaned_data["password"] == form.cleaned_data["password_again"]:
                user = models.User.objects.create_user(
                    username = form.cleaned_data['username'],
                    email = form.cleaned_data['email'],
                    password = form.cleaned_data['password']
                    )
                college=form.cleaned_data['college']

		user.is_active = False

		salt = sha.new(str(random.random())).hexdigest()[:5]
                activation_key = sha.new(salt+user.username).hexdigest()
                key_expires=datetime.datetime.today() + datetime.timedelta(2)

		user_profile = models.UserProfile(
                        user = user,
                        first_name = form.cleaned_data['first_name'].lower(),
                        last_name = form.cleaned_data['last_name'].lower(),
                        college = college,
                        mobile_number = form.cleaned_data['mobile_number'],
                        gender = form.cleaned_data['gender'],
                        age = form.cleaned_data['age'],
                        branch = clean_string(form.cleaned_data['branch']),
                        college_roll=form.cleaned_data['college_roll'],
                        want_hospi = form.cleaned_data['want_hospi'],
                        activation_key = activation_key,
                        key_expires = key_expires,
                    )
                user.save()


                try:
		    user_profile.save()
                    
                    print "*************************                  ", activation_key
                   #dont know where to get templates from. have to change this later
		    mail_template=get_template('email/activate.html')
                    body = mail_template.render(Context({'username':user.username,
							 'SITE_URL':settings.SITE_URL,
							 'activationkey':user_profile.activation_key }))
                    send_mail('Shaastra 2011 Userportal account confirmation', body,'noreply@shaastra.org', [user.email,], fail_silently=False)
                    return HttpResponseRedirect ("%sregistered/"%settings.SITE_URL)

                except:
                    user.delete();
                    user_profile.delete();
                    raise
        else: 
            form = forms.AddUserForm ()
            coll_form = forms.AddCollegeForm(prefix="id2")
	    #again have to change this later. dont know which html to use??	
            return render_to_response('users/register_user.html', locals(), context_instance= global_context(request))

def college_registration (request):
    if request.method == 'GET':
        data = request.GET.copy()
        form = forms.AddCollegeForm(data, prefix="id2")

        if form.is_valid():
            college=clean_string(form.cleaned_data['name'])
            if college.find('&')>=0:
                college = college.replace('&','and')
                city=clean_string(form.cleaned_data['city'])
                state=clean_string(form.cleaned_data['state'])

            if len (models.College.objects.filter(name=college, city=city, state=state))== 0 :
                college=models.College (name = college, city = city, state = state)
                college.save()
                return HttpResponse("created")
            else:
                return HttpResponse("exists")
        else:
            return HttpResponse("failed")
"""
@needs_authentication
@admin_only
def coord_registration(request):
    if request.method == 'POST':
        data = request.POST.copy()
        form = forms.AddCoordForm (data)
        if form.is_valid():
            if form.cleaned_data["password"] == form.cleaned_data["password_again"]:
                user = models.User.objects.create_user(
                    username = form.cleaned_data['username'],
                    email = form.cleaned_data['email'],
                    password = form.cleaned_data['password']
                    )
                #user.groups.add(models.Group.objects.get(name="Coords"))
                #user.is_staff = True
                #Need to fix this, there are more attributes for the coords model 
                coord_profile = models.coord(
                        user = user,
                        first_name = form.cleaned_data['first_name'],
                        last_name = form.cleaned_data['last_name'],
                        college = models.College.objects.get (name="Indian Institute of Technology Madras"),
                        mobile_number = form.cleaned_data['mobile_number'],
                        event_name=form.cleaned_data['event_name'],
			department=form.cleaned_data['department'],

                    )
                    #i think we should automatically assign the department based on event name.
                    # we will look into this later

                user.save()
                try:
                    coord_profile.save()

                    request.session ["registered"] = "True"

                    # we should look into this template later
                    mail_template=get_template('email/coords.html')
                    body = mail_template.render(Context({'username':user.username,'password':form.cleaned_data["password"],}))
                    send_mail('Shaastra User Portal: You have been registered as a Coordinator', body, 'no_reply@shaastra.org', [user.email,], fail_silently=False)
                    # if event:
                    #    event.coords.add(user)
                    #if team_event:
                    #    team_event.coords.add(user)
                except:
                    user.delete();
                    user_profile.delete();
                    raise 
                #have to look into this later
                return HttpResponseRedirect ("%s/register/coord/"%settings.SITE_URL)
    else: 
        form = forms.AddCoordForm ()

    # have to look into this later
    return render_to_response('registration/register_coord.html', locals(), context_instance= global_context(request)) 

@needs_authentication
def register_team (request):
    user = request.user
    if request.method == 'POST':
        data = request.POST.copy()
        form = forms.AddTeamForm (data)
        if form.is_valid():
            password = md5.new(form.cleaned_data['password']).hexdigest()
            team = models.Team (
                    name = form.cleaned_data['teamname'],
                    password = password,
                    leader = user,
                )
            team.save()
            team.members.add (user)
            team.save()
            request.session ["team_registered"] = True
            #This template is not yet made 
            mail_template=get_template('email/thankyou.html')
            body = mail_template.render(Context({'teamname':user.username,}))
            send_mail('Shaastra 11 Team Registered', body, 'noreply@shaastra.com', [user.email,], fail_silently=False)
            return HttpResponseRedirect ("%s/teams/view/%s"%(settings.SITE_URL, team.name))
    else: 
        form = forms.AddTeamForm ()
#This can be changed later if needed
    return render_to_response('registration/register_team.html', locals(), context_instance= global_context(request))

@needs_authentication
def join_team (request):
    user = request.user
    if request.method == 'POST':
        data = request.POST.copy()
        form = forms.JoinTeamForm (data)
        if form.is_valid():
            try:
                password = md5.new(form.cleaned_data['password']).hexdigest()
                team = models.Team.objects.get(
                    name = form.cleaned_data['teamname'],
                    password = password
                )
                if team in user.teams.all():
                    request.session ["already_joined"] = str(team)
                else:
                    flag=True
                    cur_len=len(team.members.all())
                    event_list=team.events.all()
                    for e in event_list:
                        if cur_len == e.size:
                            flag=False
                    if flag:

                        team.members.add (user)
                        mail_template=get_template('email/team_joined.html')
                        body = mail_template.render(Context({'teamname':team, 'team':team, 'member': request.user}))
                        send_mail('[Shaastra 2011 Userportal] Team Member Added ', body, 'noreply@shaastra.com', [request.user.email, team.leader.email], fail_silently=False)
                        team.save()
                        request.session ["team_joined"] = str(team)
                    else :
                        size_i= True
                        return render_to_response('registration/join_team.html', locals(), context_instance= global_context(request)) 
            except ObjectDoesNotExist:
                request.session ["invalid_passwd"] = form.cleaned_data["teamname"]
            return HttpResponseRedirect ("%s/teams/"%settings.SITE_URL)
    else: 
        form = forms.JoinTeamForm ()
#Can be changed later
    return render_to_response('registration/join_team.html', locals(), context_instance= global_context(request)) 

@needs_authentication
def remove_team_member (request, t_name=None, u_name=None):
    user = request.user
    teams = user.teams_lead.all()
    if t_name is None or t_name == '':
        invalid_team = session_get(request, "invalid_team")
        return HttpResponseRedirect ('%s/teams/manage/'%settings.SITE_URL)

    t_name = t_name.replace('/','')
    team = teams.filter(name=t_name)
    if not team: 
        request.session ['invalid_team'] = t_name
        return HttpResponseRedirect ('%s/teams/manage/'%settings.SITE_URL)
    team = team[0]

    if u_name is None or u_name == '':
        invalid_user = session_get(request, "invalid_user")
        return HttpResponseRedirect ('%s/teams/manage/%s'%(settings.SITE_URL,
            t_name))

    member = team.members.filter(username=u_name)

    if not member: 
        request.session ['invalid_member'] = u_name
        return HttpResponseRedirect ('%s/teams/manage/%s'%(settings.SITE_URL,
            t_name))
    member = member[0];

    if member == team.leader:
        request.session ['leader_chosen'] = u_name
        return HttpResponseRedirect ('%s/teams/manage/%s'%(settings.SITE_URL,
            t_name))

    mail_template=get_template('email/team_joined.html')
    body = mail_template.render(Context({'teamname':team, 'team':team, 'member': request.user}))
    send_mail('[Shaastra 11 Userportal] Team Member Removed ', body, 'noreply@shaastra.com', [member.email, team.leader.email], fail_silently=False)

    team.members.remove(member)
    request.session ['remove_success'] = u_name

    return HttpResponseRedirect ('%s/teams/manage/%s'%(settings.SITE_URL,t_name))

def activate (request, a_key = None ):
    SITE_URL = settings.SITE_URL
    if (a_key == '' or a_key==None):
	key_dne = True
	return render_to_response('registration/activated.html',locals(), context_instance= global_context(request))
    else:
        try:
            user_profile = models.UserProfile.objects.get(activation_key = a_key)
        except ObjectDoesNotExist:
            prof_dne = True
            return render_to_response('registration/activated.html',locals(), context_instance= global_context(request))

        #Cleanup operation
        if user_profile.key_expires < datetime.datetime.today():
            expired = True
            user = user_profile.user
            user.delete()
            user_profile.delete()
            return render_to_response('registration/activated.html',locals(), context_instance= global_context(request))

        else:
            user = user_profile.user
            user.is_active = True
            user.save()
            request.session["registered"]=True

            #send another mail
            mail_template=get_template('email/thankyou.html')
            body = mail_template.render(Context({'username':user.username}))
            send_mail('Account activated', body, 'noreply@shaastra.org', [user.email,], fail_silently=False)

            #print "IS AUTHENTICATED",user.is_authenticated()
            activated = True
            return render_to_response('registration/activated.html',locals(), context_instance= global_context(request))

@needs_authentication
def manage_teams (request, t_name = None):
    user = request.user
    teams = user.teams_lead.all()
    if t_name is None or t_name == '':
        invalid_team = session_get(request, "invalid_team")
        invalid_passwd = session_get(request, "invalid_passwd")
        return render_to_response('registration/manage_list_teams.html', locals(), context_instance= global_context(request)) 
    t_name = t_name.replace('/','')

    team = teams.filter(name=t_name)
    if not team: 
        request.session ['invalid_team'] = t_name
        return HttpResponseRedirect ('%s/manage_teams/'%settings.SITE_URL)

    remove_success = session_get(request, "remove_success")
    invalid_member = session_get(request, "invalid_member")
    leader_chosen = session_get(request, "leader_chosen")
    team = team[0]
    members = team.members.all()

    return render_to_response('registration/manage_team_members.html', locals(), context_instance= global_context(request)) 

@needs_authentication 
def profile(request):
    user = request.user
    userprof=request.user.get_profile()
    if request.method=="POST":
        data=request.POST.copy()        
        form1 = forms.ModifyUserForm (prefix='1', instance=user, data=data)
        form2 = forms.ModifyUserProfileForm (prefix='2', instance=userprof, data=data)
        if form1.is_valid() and form2.is_valid():
            if form1.cleaned_data["password1"] != '':
                user.set_password(form1.cleaned_data["password1"])
            user.email = form1.cleaned_data["email"]
            user.save()
            userprof.profile_not_set=False
            userprof.save()
            form2.save()
            request.session['success'] = True
            return HttpResponseRedirect (request.path)
    else:
        form1 = forms.ModifyUserForm (prefix='1', instance=user)
        form2 = forms.ModifyUserProfileForm (prefix='2', instance=userprof)
        print form2.as_table

    success = session_get(request,'success')

    return render_to_response('registration/profile.html', locals(), context_instance= global_context(request)) 


@needs_authentication
@coords_only
def edit_profile (request, u_id=None):
    if (not u_id):
        if request.method=="POST":            
            data = request.POST.copy()       
            form = forms.SelectUserForm (data = data)
            if form.is_valid():
                userid = form.cleaned_data["shaastra_id"]
                try:    
                    participant = models.User.objects.get(id=userid)
                except ObjectDoesNotExist:
                    return HttpResponseRedirect ('%s/edit_profile/%s/'%(settings.SITE_URL,userid))
                uprof = participant.get_profile()
                if (form.cleaned_data["user_email"]):
                    mail = form.cleaned_data["user_email"]
                    u = models.User.objects.filter(email=mail)
                    if (not u):
                        uprof.user.email=mail
                        uprof.id_type = "onthespot"
                        uprof.user.save()
                        uprof.save()

                    if u:
                        uprof.id_type = "onthespot-portaluser"
                        uprof.user.email=mail
                        uprof.user.save()
                        uprof.save()
                        request.session["mail_id_present"]=True 
                else:
                    uprof.id_type = "onthespot"
                    uprof.save()
                return HttpResponseRedirect ('%s/edit_profile/%s/'%(settings.SITE_URL,userid))

        else:
            form = forms.SelectUserForm ()
        success = session_get(request,'success')

        return render_to_response('registration/select_profile.html', locals(), context_instance= global_context(request)) 

    try:
        participant = models.User.objects.get(id=u_id)
    except ObjectDoesNotExist:
        request.session["invalid_user"] = u_id
        return HttpResponseRedirect ('%s/profile/'%settings.SITE_URL)
    userprof=participant.get_profile()
    if request.method=="POST":
        data=request.POST.copy()       
        form = forms.ModifyCompleteUserProfileForm (instance=userprof, data=data)
        form.save()
        request.session['success'] = True
        return HttpResponseRedirect ('%s/edit_profile/'%(settings.SITE_URL))
    else:
        form = forms.ModifyCompleteUserProfileForm (instance=userprof)
    success = session_get(request,'success')
    flag_email = session_get(request,'mail_id_present')

    return render_to_response('registration/edit_profile.html', locals(), context_instance= global_context(request)) 

@coords_only
@needs_authentication 
def super_profile(request, u_name):
    user = request.user
    u_name = u_name.replace("/","")
    try:
        participant = models.User.objects.get(username=u_name)
    except ObjectDoesNotExist:
        request.session["invalid_user"] = u_name
        return HttpResponseRedirect ('%s/profile/'%settings.SITE_URL)

    participant_prof=participant.get_profile()
    selected_events = models.Submission.objects.filter(user = participant, selected = True)
    teams = participant.teams.all()
    print teams
    selected_team_events = []
    for team in teams:
        selected_team_events  += models.TeamSubmission.objects.filter(team=team, selected=True)
    print selected_events,selected_team_events
    return render_to_response('registration/super_profile.html', locals(), context_instance= global_context(request)) 

@needs_authentication
def change_password(request,t_name = None):

    user = request.user
    if t_name is None or t_name == '':
        invalid_team = session_get(request, "invalid_team")
        invalid_passwd = session_get(request, "invalid_passwd")
        return render_to_response('registration/manage_list_teams.html', locals(), context_instance= global_context(request)) 

    t_name = t_name.replace('/','')
    team = models.Team.objects.filter(name=t_name)
    pwd=''
    incorrect_password=False
    if team:
        team=team[0]
    if request.method == 'POST':
        try:
            if request.POST['password1'] == request.POST['password2']:
                print "hi"
                pwd = request.POST.get('password1','')
            else:
                incorrect_password=True
        except:
            pass
        print pwd
        if pwd:
            team.password = md5.new(pwd).hexdigest()
            team.save()
            return HttpResponseRedirect ('%s/teams/manage/'%settings.SITE_URL)

    return render_to_response('registration/team_changepwd.html',locals(), context_instance= global_context(request)) 

@needs_authentication
def view_teams (request, t_name = None):
    user = request.user
    teams = user.teams.all()
    if t_name is None or t_name == '':
        invalid_team = session_get(request, "invalid_team")
        invalid_passwd = session_get(request, "invalid_passwd")
        return render_to_response('registration/list_teams.html', locals(), context_instance= global_context(request)) 
    else:
	#Comment out the following two lines when event registrations are open
	#not_started = True
	#return render_to_response('home/home.html',locals(),context_instance= global_context(request))
        t_name = t_name.replace('/','')

        if not teams.filter(name=t_name): 
            request.session ['invalid_team'] = t_name
            return HttpResponseRedirect ('%s/teams/'%settings.SITE_URL)

        else:
            team = teams.get(name=t_name)
            events_list = models.TeamEvent.objects.filter(registerable=True)
            list1=[]
            list2=[]
            show_hospi = False
            for usr in team.members.all():
                if usr.get_profile().want_hospi :
                    show_hospi=True
                    break

            for e in events_list:
                if e.hospi_only :
                    list1.append(e)
                else :
                    list2.append(e)

            events= []
            events1=[]
            events2=[]

            invalid_event = session_get(request, "invalid_event")
            event_success = session_get(request,"event_success")

            for event in events_list:
                events.append ((camelize(event.name),event,len(event.teams.filter(name=team))))

            for event in list1:
                events1.append ((camelize(event.name),event,len(event.teams.filter(name=team)) >0))

            for event in list2:
                events2.append ((camelize(event.name),event,len(event.teams.filter(name=team)) >0))

            return render_to_response('registration/list_team_events.html', locals(), context_instance= global_context(request))         
"""
