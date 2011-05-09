# have written a very basic crude definition of events_all model




from django.db import models
from django.contrib import admin
from django import forms
from main_test.users.models import *

# Create your models here.

class Tag(models.Model):
    name=models.CharField(max_length=30)
    def __str__(self):
        return self.name
    
    class Admin:
        pass

class image_for_tabs(models.Model):
    image=ImageField(upload_to="public_html/2011/media/") #how to avoid file conflicts ? Files with same name
    
class Tabs(models.Model):
    content=models.TextField()
    tabimage=models.ManyToManyField(image_for_tabs)  #One tab may have multiple images. We don't know how many
    #Have yet to write questions and discussion forums classes 
         
class event(models.Model):
    
    name = models.CharField(max_length=100)
    url = models.URLField(null=True,verify_exists=False, blank=True)
    start_time = models.DateTimeField(null=True,blank=True)
    end_time = models.DateTimeField(null=True,blank=True)
    registerable = models.BooleanField()
    users = models.ManyToManyField(generic_user, related_name='events', blank=True, null=True)
    chosen_users = models.ManyToManyField(generic_user, blank=True, null=True, related_name='qualified_events')
    flagged_by = models.ManyToManyField(generic_user,blank=True, null= True, related_name='flagged_events')
    logo = models.FileField(upload_to="logos/", blank=True, null=True)
    tabs = models.ForeignKey(Tabs)
    event_type = models.TextField(max_length=30) #Could be bool field also
    #Many to Many or foreign key ? I dunno
    # OR tabs=models.XMLField()
    #Defined tabs as an XML field. Thought it would be easier to handle an XML file. I don't know how to write to view for this yet. We need to find out 
    
    def __str__(self):
        return self.name

    class Admin:
        pass
    






