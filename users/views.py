
# Create your views here.

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.contrib.auth.models import User, Group
from django.template.loader import get_template
from django.template.context import Context, RequestContext
from django.utils.translation import ugettext as _
from django.core.mail import send_mail,EmailMessage,SMTPConnection
from django.contrib.sessions.models import Session
from django.utils import simplejson

from main_test.misc.util import *
from main_test.settings import *
from main_test.users.models import UserProfile, College
from main_test.users import models
from main_test.users import forms

import sha,random,datetime
def login (request):
    form=forms.LoginForm()
    if 'logged_in' in request.session and request.session['logged_in'] == True:
        return HttpResponseRedirect("%sevents/dashboard/" % settings.SITE_URL)
    if request.method == 'POST':
        data = request.POST.copy()
        form = forms.LoginForm(data)
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
                return render_to_response('users/login.html', locals(), context_instance= global_context(request))
                
        else:                       
            invalid_login = session_get(request, "invalid_login")
            form = forms.LoginForm () 
    return render_to_response('users/login.html', locals(), context_instance= global_context(request))
    
def logout(request):
    if request.user.is_authenticated():
        auth.logout (request)
        return render_to_response('users/logout.html', locals(), context_instance= global_context(request))        
    return HttpResponseRedirect('%sevents/login/'%settings.SITE_URL)        
    
def user_registration(request):
    colls = models.College.objects.all()
    collnames = list()
    for coll in colls:
        collnames.append(coll.name + "," + coll.city)
    js_data = simplejson.dumps(collnames)
    
    blue = "HAHAHAHAHA HIHIHIHI HUHUHUHU HEHEHEHE"
    if request.method=='POST':
        data = request.POST.copy()
        form = forms.AddUserForm(data)
  
        if form.is_valid():
  
            user = User.objects.create_user(username = form.cleaned_data['username'], email = form.cleaned_data['email'],password = form.cleaned_data['password'],)
            user.is_active = False
            user.save()
            salt = sha.new(str(random.random())).hexdigest()[:5]
            activation_key = sha.new(salt+user.username).hexdigest()
            key_expires=datetime.datetime.today() + datetime.timedelta(2)

            userprofile = UserProfile(
                    user = user,
                    gender     = form.cleaned_data['gender'],
                    age = form.cleaned_data['age'],
                    branch = form.cleaned_data['branch'],
                    mobile_number = form.cleaned_data['mobile_number'],
                    college =form.cleaned_data['college'],
                    college_roll = form.cleaned_data['college_roll'],
                    shaastra_id  = user.id , # is this right
                    activation_key = activation_key,
                    key_expires  = key_expires,
                    )
            userprofile.save()
            mail_template=get_template('email/activate.html')
            body = mail_template.render(Context({'username':user.username,
							 'SITE_URL':settings.SITE_URL,
							 'activationkey':userprofile.activation_key }))
            send_mail('Your new Shaastra2011 account confirmation', body,'noreply@shaastra.org', [user.email,], fail_silently=False)

    else:
        form = forms.AddUserForm()
        coll_form = forms.AddCollegeForm(prefix="identifier")
    return render_to_response('users/register_user.html', locals(), context_instance= global_context(request))    
                            
def college_registration (request):
    if request.method == 'GET':
        data = request.GET.copy()
        coll_form = forms.AddCollegeForm(data,prefix="identifier")

        if coll_form.is_valid():
            college=clean_string(coll_form.cleaned_data['name'])
            if college.find('&')>=0:
                college = college.replace('&','and')
            city=clean_string(coll_form.cleaned_data['city'])
            state=clean_string(coll_form.cleaned_data['state'])

            if len (College.objects.filter(name=college, city=city, state=state))== 0 :
                college=College (name = college, city = city, state = state)
                college.save()
                data = college.name+","+college.city
                #return HttpResponse("created") 
                return HttpResponse(data, mimetype="text/plain")


            else:
                return HttpResponse("exists")
        else:
            return HttpResponse("failed")
    #redundant as registration done by ajax call....
    #else:
    #coll_form=forms.AddCollegeForm()        
    #return render_to_response('users/register_user.html', locals(), context_instance= global_context(request))        
            
def activate (request, a_key = None ):
    SITE_URL = settings.SITE_URL
    if (a_key == '' or a_key==None):
	    key_dne = True
	    
    else:
        try:
	        user_profile = UserProfile.objects.get(activation_key = a_key)
        except ObjectDoesNotExist:

            prof_dne = True
        if user_profile.key_expires < datetime.datetime.today():
	        expired = True
	        user = user_profile.user
	        user.delete()
	        user_profile.delete()
	
        else:
            user = user_profile.user
            user.is_active = True
            user.save()
            request.session["registered"]=True
            activated = True

    return render_to_response('registration/activated.html',locals(), context_instance= global_context(request))
    

@needs_authentication
def myshaastra(request):
    user = request.user
    userprof = user.get_profile()
    events_list = userprof.registered
    return render_to_response('my_shaastra.html', locals(), context_instance = global_context(request))

