
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
from main_test.registration.php_serialize.PHPSerialize import *
from main_test.registration.models import UserProfile
import models,forms
import sha,random,datetime

def login_user(request):

    redirected = request.session.get ("from_url", False)
    registered = session_get (request, "registered")
    form = forms.UserLoginForm ()
    username = password = ''
    if request.method == 'POST':
        data = request.POST.copy()
	  if request.POST.get('from_url',False):
	    request.session['from_url']='http://www.shaastra.org/2010/helpdesk/forum.php?req=setuser'
	    #Obviously needs fixing. :P
	    print request.session['from_url']
      else:
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
            else:
                request.session['invalid_login'] = True
                return HttpResponseRedirect (request.path)
    else: 
        invalid_login = session_get(request, "invalid_login")
        form = forms.UserLoginForm ()

    return render_to_response('home/login.html', locals(), context_instance= global_context(request)) 
    

# just copied the user registration
# i dont think much of changes required 


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

				user_profile = models.User(
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
                    try:
						unb_register (user, form.cleaned_data['password'])
                    except:
						pass
                    
                    print "*************************                  ", activation_key
                   #dont know where to get templates from. have to change this later
				   mail_template=get_template('email/activate.html')
                    body = mail_template.render(Context({'username':user.username,
							 'SITE_URL':settings.SITE_URL,
							 'activationkey':user_profile.activation_key }))
                    send_mail('Shaastra 2011 Userportal account confirmation', body,'noreply@shaastra.org', [user.email,], fail_silently=False)
                    return HttpResponseRedirect ("%s/home/registered/"%settings.SITE_URL)

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
  
          
            if len (models.College.objects.filter(
                name=college,
                city=city,
                state=state))== 0 :
				college=models.College (
                     name = college,
                     city = city,
                     state = state
                     )
                college.save()
                return HttpResponse("created")
            else:
                return HttpResponse("exists")
        else:
            return HttpResponse("failed")

		
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

                coord_profile = models.coord(
                        user = user,
                        first_name = form.cleaned_data['first_name'],
                        last_name = form.cleaned_data['last_name'],
                        college = models.College.objects.get (name="Indian Institute of Technology Madras"),
                        mobile_number = form.cleaned_data['mobile_number'],
                        event_name=form.cleaned_data['event_name']
						department=form.cleaned_data['department']
                    )
				#i think we should automatically assign the department based on event name.
			    # we will look into this later

                user.save()
                try:
                    coord_profile.save()
                    
                    request.session ["registered"] = "True"
                    unb_register (user, form.cleaned_data['password'], True)#We don't need this do we?

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

