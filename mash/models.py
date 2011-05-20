from django.db import models
from main_test.users.models import *
from django import forms

class photos(models.Model):
    photolink      = models.URLField()
    photoid        = models.AutoField(primary_key=True)
    rating         = models.FloatField (max_digits=7,decimal_places=2)
    groupnum       = models.IntegerField(blank=False, null=False)
    photo          = models.ImageField(upload_to=('/galleryfinal/%s',photoid)
    user           = models.Foreignkey(User)
    
    def __str__(self):
        return str(self.photoid)
#Since photoid is an autofield it ll automatically increment and each photo will have a unique photo id. It ll be saved to galleryfinal/[photoid].jpg . The photo can be accessed with the help of the photo id. 

#This is the form for uploading
class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file  = forms.FileField()


