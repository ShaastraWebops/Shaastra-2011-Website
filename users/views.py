
# Create your views here.

from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect

from django.template.loader import get_template
from django.template.context import Context, RequestContext

import forms
from main_test.users import models
import sha, random, datetime

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

                   

