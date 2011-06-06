
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

from main_test.misc.util import *
from main_test.settings import *
from main_test.users.models import UserProfile, College
#from main_test.users import models
from main_test.users import forms

import sha,random,datetime

def user_registration(request):

    if request.method=='POST':
        data = request.POST.copy()
        form = forms.AddUserForm(data)
  
        if form.is_valid():
  
            user = User.objects.create_user(username = form.cleaned_data['username'], email = form.cleaned_data['email'],password = form.cleaned_data['password'],)
            user.is_active = False;
            try:
                user.save()
                salt = sha.new(str(random.random())).hexdigest()[:5]
                activation_key = sha.new(salt+user.username).hexdigest()
                key_expires=datetime.datetime.today() + datetime.timedelta(2)
            
                user_profile = models.UserProfile (
                        user = user,
                        first_name = form.cleaned_data['first_name'].lower(),
                        last_name = form.cleaned_data['last_name'].lower(),
                        college = college,
                        mobile_number = form.cleaned_data['mobile_number'],
                        gender = form.cleaned_data['gender'],
                        age = form.cleaned_data['age'],
                        email_id = form.cleaned_data['email'],
                        branch = clean_string(form.cleaned_data['branch']),
                        college_roll=form.cleaned_data['college_roll'],
                        want_hospi = form.cleaned_data['want_hospi'],
                        activation_key = activation_key,
                        key_expires = key_expires,
                        is_coord = False,
                    )
                try:
                    user_profile.save()
                except:
                    print "error_ 2"                
            except:
                print "error_1"
    else:
        form = forms.AddUserForm()
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

@needs_authentication
def myshaastra(request):
    user = request.user
    userprof = user.get_profile()
    events_list = userprof.registered
    return render_to_response('my_shaastra.html', locals(), context_instance = global_context(request))

