# coding: utf-8
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
import StringIO
import hashlib
from datetime import datetime
from tempfile import NamedTemporaryFile, mkdtemp
import Image
from main_test.misc.util import *
from math import fabs

TECHMASH_URL = 'http://www.shaastra.org/2011/media/techmash/'
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("%stechmash/accounts/login/" % settings.SITE_URL)
    else:
        form = UserCreationForm()
        c={'form':form}
    return render_to_response("registration/register.html",locals(),context_instance= global_context(request))

def profile(request):
 	return render_to_response("techmash/profile.html", locals(),context_instance= global_context(request))

def upload_file1(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print "form valid"
            destdir= os.path.join(settings.TECHMASH_ROOT,'images/')
            if not os.path.isdir(destdir):
                os.makedirs(destdir, 0775)
            i=request.FILES['file']
            str = ''
            for c in i.chunks():
                str += c
            imagefile  = StringIO.StringIO(str)
            imageImage = Image.open(imagefile)
            filename = hashlib.md5(imagefile.getvalue()).hexdigest()+'.jpg'
            destdir= os.path.join(settings.TECHMASH_ROOT,'images/')
            if not os.path.isdir(destdir):
                os.makedirs(destdir, 0775)
            photopath = os.path.join(destdir, os.path.basename(filename))
            fout = open(photopath, 'wb+')
            f=request.FILES['file']
            for chunk in f.chunks():
                fout.write(chunk)
            fout.close()         
            #print photopath
            # Create the object
            if photopath.startswith(os.path.sep):
                photopath = photopath[len(settings.TECHMASH_ROOT):]
            photo = Photo(image=photopath,title = filename,rating=1600,kvalue = 32, user=request.user.username)
            # Save it -- the thumbnails etc. get created.
            photo.save()
            handle_uploaded_image(request.FILES['file'])
            return HttpResponseRedirect(("%stechmash/upload/" % settings.SITE_URL))
    else:
        form = UploadFileForm()
        return render_to_response('techmash/upload_file.html', locals(),context_instance= global_context(request))

def kvaluegenerator(rating):
    kdictionary = { 0 : 36 , 1: 34 , 2:32 , 3:30 , 4:28 , 5:26 , 6:24 , 7:22 , 8:20 , 9:18 , 10:16 }
    factor = 0 
    if rating > 1400:
        factor = int(((rating - 1400)/100))
    return kdictionary[factor]            

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
            photo1winprob= 1/((10**(( rphoto2.rating-rphoto1.rating)/400)) + 1)
            photo2winprob= 1/((10**(( rphoto1.rating-rphoto2.rating)/400)) + 1)
            if selectedid==photoid1:
                rphoto1.rating = rphoto1.rating + (rphoto1.kvalue * (1-photo1winprob))
                rphoto2.rating = rphoto2.rating + (rphoto2.kvalue * (0-photo2winprob))
            else:
                rphoto2.rating = rphoto2.rating + (rphoto2.kvalue * (1-photo2winprob))
                rphoto1.rating = rphoto1.rating + (rphoto1.kvalue * (0-photo1winprob))
            rphoto1.kvalue = kvaluegenerator(rphoto1.rating)
            rphoto2.kvalue = kvaluegenerator(rphoto2.rating)                                
            rphoto1.save()
            rphoto2.save()
            photo1,photo2=selectimages(request)
            return render_to_response("techmash/select.html", locals(),context_instance= global_context(request))
        else:
            photo1,photo2=selectimages(request)
            return render_to_response("techmash/select.html", locals(),context_instance= global_context(request))    
    else:
        photo1,photo2=selectimages(request)
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
    photo1=Photo.objects.order_by('?')[0]
    print photo1.title
    photo2=Photo.objects.filter(kvalue=photo1.kvalue).order_by('?')[0]
    return(photo1,photo2)

def seephotos(request):   
    photo_list=Photo.objects.all()
    return render_to_response("techmash/mash.html", locals(),context_instance= global_context(request))

def handle_uploaded_image(i):
    str = ''
    for c in i.chunks():
        str += c
    imagefile  = StringIO.StringIO(str)
    photo = Image.open(imagefile)
    resizedImage = photo.thumbnail((400, 400),Image.ANTIALIAS)
    imagefile = StringIO.StringIO()
    resizedImage.save(imagefile,'JPEG')
    filename = hashlib.md5(imagefile.getvalue()).hexdigest()+'.jpg'
    destdir= os.path.join(settings.TECHMASH_ROOT,'images/')
    if not os.path.isdir(destdir):
        os.makedirs(destdir, 0775)
    photopath = os.path.join(destdir, os.path.basename(filename))
    fout = open(photopath, 'wb+')
    imagefile = open(photopath, 'w')
    resizedImage.save(imagefile,'JPEG')
