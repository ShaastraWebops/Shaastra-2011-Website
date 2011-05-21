# Create your views here.
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, Http404, HttpResponseRedirect
import datetime
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from mash.models import UploadFileForm
from django import forms
import os


#This is the view for uploading to the given path    
def upload_file1(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            folder = request.path.replace("/", "_")
            uploaded_filename = request.FILES['file'].name

    # create the folder if it doesn't exist.
            try:
                os.mkdir(os.path.join('/home/chinmay/mysite/', folder))
            except:
                pass

    # save the uploaded file inside that folder.
            full_filename = os.path.join('/home/chinmay/mysite/', folder, uploaded_filename)
            fout = open(full_filename, 'wb+')
            f=request.FILES['file']
            for chunk in f.chunks():
                fout.write(chunk)
                fout.close()

            return HttpResponseRedirect('/upload')
    else:
        form = UploadFileForm()
    return render_to_response('uploaded_file.html', {'form': form})

    

