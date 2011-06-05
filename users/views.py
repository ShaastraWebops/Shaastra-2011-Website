
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

import sha,random,datetime

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

