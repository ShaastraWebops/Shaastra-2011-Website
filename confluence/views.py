# Create your views here.

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import get_template
from django.template.context import Context, RequestContext

from main_test.misc.util import *
from main_test.settings import *
from main_test.confluence.models import RSVP 
from main_test.confluence import forms

def rsvp(request):

    if request.method=='POST':
        data = request.POST.copy()
        form = forms.RSVPForm(data)
  
        if form.is_valid():
  
            
            RSVPdata = RSVP(
                    name = form.cleaned_data['name'],
                    address = form.cleaned_data['address'],
                    mobile_number = form.cleaned_data['mobile_number'],
		    email = form.cleaned_data['email'],	
                    )
	    RSVPdata.save()            
            return render_to_response('users/confluence_reg.html', locals(), context_instance= global_context(request))
        else: 
            print form.errors  
            return render_to_response('users/confluence.html' , locals() ,context_instance = global_context(request))
    else:
        form = forms.RSVPForm()

    
    
    return render_to_response('users/confluence.html', locals(), context_instance= global_context(request))
