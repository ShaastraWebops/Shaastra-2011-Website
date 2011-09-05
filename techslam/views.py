# coding: utf-8
# Word of advice - Don't read the code. Rewrite it. It sucks. 
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from main_test.techslam.models import *
from django import forms
from django.contrib.auth.decorators import login_required
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

TECHMASH_URL = 'http://www.shaastra.org/2011/media/techslam/'
def profile(request,username=None):
    if username == "myprofile":
        if request.user.is_authenticated():
            username = request.user.username
        else:
            return HttpResponseRedirect(settings.SITE_URL + "login")    
    if username == request.user.username:
        show_buttons = True          
    try:
        image_list = Photo.objects.filter(user = username).order_by('rating')
    except:
        image_list =list()    
    return render_to_response("techslam/techslam.html", locals(),context_instance= global_context(request))

def spons_backend(request):
    image_list = Photo.objects.order_by('photoid').reverse()
    return render_to_response("techslam/spons.html", locals(),context_instance = global_context(request))

def top_photos(request):
    try:
        image_list = Photo.objects.order_by('rating')
    except:
        image_list =list()    
    return render_to_response("techslam/top_photos.html", locals(),context_instance= global_context(request))
    
@needs_authentication 	
def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            destdir= os.path.join(settings.TECHMASH_ROOT,'images/')
            if not os.path.isdir(destdir):
                os.makedirs(destdir, 0775)
            i=request.FILES['file']
            str = ''
            for c in i.chunks():
                str += c
            imagefile  = StringIO.StringIO(str)
            photo = Image.open(imagefile)
            photo.thumbnail((400, 400),Image.ANTIALIAS)
            hashcode = hashlib.md5(imagefile.getvalue()).hexdigest()
            filename = hashcode +'.jpg'
            destdir= os.path.join(settings.TECHMASH_ROOT,'images/')
            if not os.path.isdir(destdir):
                os.makedirs(destdir, 0775)
            photopath = os.path.join(destdir, os.path.basename(filename))
            fout = open(photopath, 'wb+')
            imagefile = open(photopath, 'w')
            photo.save(imagefile,'JPEG')
            # Create the object
            if photopath.startswith(os.path.sep):
                photopath = photopath[len(settings.TECHMASH_ROOT):]
            photo = Photo(image=photopath,title = filename,rating=1600,kvalue = 32, user=request.user.username,caption=form.cleaned_data['caption'])
            # Save it -- the thumbnails etc. get created.
            photo.save()
            #handle_uploaded_image(request.FILES['file'])
            return HttpResponseRedirect(("%stechslam/upload/" % settings.SITE_URL))
        else:
            return HttpResponseRedirect(("%stechslam/upload/" % settings.SITE_URL))   
    else:
        form = UploadFileForm()
        return render_to_response('techslam/upload_file.html', locals(),context_instance= global_context(request))

def kvaluegenerator(rating):
    kdictionary = { 0 : 36 , 1: 34 , 2:32 , 3:30 , 4:28 , 5:26 , 6:24 , 7:22 , 8:20 , 9:18 , 10:16 }
    factor = 0 
    if rating > 1400:
        factor = int(((rating - 1400)/100))
    return kdictionary[factor]            

def slamphotos(request):
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
            photo1,photo2=selectimages()
            return render_to_response("techslam/compare.html", locals(),context_instance= global_context(request))
        else:
            photo1,photo2=selectimages()
            return render_to_response("techslam/compare.html", locals(),context_instance= global_context(request))    
    else:
        photo1,photo2=selectimages()
        return render_to_response("techslam/compare.html", locals(),context_instance= global_context(request))

def deleteimage(request,image_title=None):
    try:
        photo_to_delete = Photo.objects.get(title = image_title)
        if request.user.username == photo_to_delete.user:
            try:
                photo_to_delete.delete()
            except:
                pass    
        else:
            pass
    except:
        pass            
    return HttpResponseRedirect(settings.SITE_URL + 'techslam/' + request.user.username + '/showprofile/')
    
def selectimages():
    photo1=Photo.objects.order_by('?')[0]
    try:
        photo2=Photo.objects.filter(kvalue=photo1.kvalue).exclude(photoid=photo1.photoid).order_by('?')[0]
    except:
        pass    
    return(photo1,photo2)

def render_static(request,static_name):
    if static_name=="landing":
        return render_to_response('techslam/landing.html', locals(), context_instance = global_context(request)) 
    if static_name=="about":
        return render_to_response('techslam/about.html', locals(), context_instance = global_context(request)) 
    if static_name=="rules":
        return render_to_response('techslam/rules.html', locals(), context_instance = global_context(request)) 
    if static_name=="prizes":
        return render_to_response('techslam/prizes.html', locals(), context_instance = global_context(request))
    if static_name=="elo":
        return render_to_response('techslam/elo.html', locals(), context_instance = global_context(request))
