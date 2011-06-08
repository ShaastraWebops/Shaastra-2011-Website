# Create your views here.
# Create your views here.
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from main_test.techmash.models import *
from django import forms
import os
import stat
import shutil
from datetime import datetime
from tempfile import NamedTemporaryFile, mkdtemp
import Image
from main_test.misc.util import *
from math import fabs

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("%stechmash/accounts/login/" % settings.SITE_URL)
    else:
        form = UserCreationForm()
        c={'form':form)
    return render_to_response("registration/register.html",locals(),context_instance= global_context(request))

def profile(request):
 	return render_to_response("techmash/profile.html", Context({'usename': request.user.username}), locals(),context_instance= global_context(request))

def upload_file1(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print "form valid"
            uploaded_filename = request.FILES['file'].name
            destdir= os.path.join(settings.MEDIA_ROOT,'images/')
            if not os.path.isdir(destdir):
                os.makedirs(destdir, 0775)
            photopath = os.path.join(destdir, os.path.basename(uploaded_filename))
            fout = open(photopath, 'wb+')
            f=request.FILES['file']
            for chunk in f.chunks():
                fout.write(chunk)
            fout.close()         
            print photopath
            # Create the object
            if photopath.startswith(os.path.sep):
                photopath = photopath[len(settings.MEDIA_ROOT):]
            photo = Photo(image=photopath,title = uploaded_filename,rating=300,user=request.user.username,groupnum=1)
            # Save it -- the thumbnails etc. get created.
            photo.save()
            return HttpResponseRedirect(("%stechmash/upload/" % settings.SITE_URL))
    else:
        form = UploadFileForm()
        return render_to_response('techmash/upload_file.html', Context({'form': form}), locals(),context_instance= global_context(request))

def mashphotos(request):
    if request.method == 'POST':
        form = selectaphoto(request.POST)
        print "request method post"
        if form.is_valid():    
            print "form valid"
            selectedid=request.POST['selectedid']
            photoid1=request.POST['photoid1']
            photoid2=request.POST['photoid2']
            rphoto1=Photo.objects.get(photoid=photoid1)
            rphoto2=Photo.objects.get(photoid=photoid2)
            rphoto3=Photo.objects.get(photoid=selectedid)
            print rphoto1.rating
            print rphoto2.rating
            print rphoto3.rating
            diff=fabs(rphoto1.rating-rphoto2.rating)
            if diff==0:
                rphoto3.rating=rphoto3.rating+10
            elif rphoto3.rating<500:
                rphoto3.rating=rphoto3.rating+diff*10
            elif rphoto3.rating<1000:                                                                                                                                                           
                rphoto3.rating += diff*8   
            else:
                rphoto3.rating +=diff*5
            print "here u are"
            photo1,photo2=selectimages(request)
            print rphoto3.rating
            rphoto3.save()
            return render_to_response("techmash/select.html", locals(),context_instance= global_context(request))
        else:
            photo1,photo2=selectimages(request)
            print "here i am2"
            return render_to_response("techmash/select.html", locals(),context_instance= global_context(request))    
    else:
        photo1,photo2=selectimages(request)
        print "here i am2"
        return render_to_response("techmash/select.html", locals(),context_instance= global_context(request))



def updategrp(self):
    photo.objects.order_by(rating)
    q = photo.objects.annotate(number_of_entries=Count('entry'))
    a=q[0].number_of_entries
    a1=a/10                     #Sorts in ascending order
    j=0
    k=0
    m=0
    aint=int(a1)+1    
    while  j<a:
       while m<aint:
           photohere=photo(photo.id)
           photohere.group=k
           m=m+1 
       k=k+1     
       m=m-aint

from random import randint, choice

def selectimages(request):
    group=1
    photo_list=Photo.objects.all().order_by('?')[:2]                    
    print photo_list
    photo1=photo_list[0:1].get()
    photo2=photo_list[1:2].get()
    print "here"
    return(photo1,photo2)
    #show2=pool.objects.filter(random 2)
    #give to template#

def seephotos(request):   
    photo_list=Photo.objects.all()
    return render_to_response("techmash/mash.html", locals(),context_instance= global_context(request))
