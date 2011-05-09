# have written a very basic crude definition of events_all model




from django.db import models
from django.contrib import admin
from django import forms
from main_test.users.models import *

# Create your models here.

class event(models.Model):
    
    name = models.CharField(max_length=100)
    url = models.URLField(null=True,verify_exists=False, blank=True)
    start_time = models.DateTimeField(null=True,blank=True)
    end_time = models.DateTimeField(null=True,blank=True)
    registerable = models.BooleanField()
    users = models.ManyToManyField(generic_user, related_name='events', blank=True, null=True)
    chosen_users = models.ManyToManyField(generic_user, blank=True, null=True, related_name='qualified_events')
    logo=models.FileField(upload_to="logos/", blank=True, null=True)
    
    def __str__(self):
        return self.name

    class Admin:
        pass
    
class Tag(models.Model):
    name=models.CharField(max_length=30)
    def __str__(self):
        return self.name
    
    class Admin:
        pass





