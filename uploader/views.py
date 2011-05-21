from django import forms

from django.shortcuts import render_to_response

from django.http import HttpResponseRedirect
from techmash.mash.models import UploadFileForm

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('upload_file.html')
    else:
        form = UploadFileForm()
    return render_to_response('upload_file.html', {'form': form})

def handle_uploaded_file(f):
    destination = open('home/chinmay/main_test/uploader/name.txt', 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
        destination.close()
