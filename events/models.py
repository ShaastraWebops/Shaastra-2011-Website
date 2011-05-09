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
    image=models.ImageField(upload_to="public_html/2011/media/") #how to avoid file conflicts ? Files with same name can't be stored in same directory
    
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
    event_type = models.TextField(max_length=30) #Could be bool field also
    tabs = models.ForeignKey(Tabs)
    #Many to Many or foreign key ? I dunno
    # OR tabs=models.XMLField()
    #We could define tabs as an XML field in event itself. Thought it would be easier to handle an XML file. I don't know how to write to view for this yet. We need to find out 
    
    def __str__(self):
        return self.name

    class Admin:
        pass
#This is just last years code for questions. Need to think of ways to make it better    
class Question(models.Model):
    TYPE = (
            (1, 'Normal'),
            (2, 'File'),
            (3, 'MCQ'),
            #(4, 'Message'),
            )
    
    event = models.ForeignKey(event)
    content = models.TextField(max_length=1000)
    pref_id = models.IntegerField(blank= False, null = False ,verbose_name = 'Question Number. Note that this will be the number displayed in the button for this question.',)
    type = models.IntegerField(choices=TYPE)
    visible = models.BooleanField(default=True)
    def __str__(self):
        return self.content
    def get_choices (self):
        if self.type != 3:
            raise ValueError
        list = MCQOption.objects.filter(question=self)
        choices = []
        num = 1
        for option in list:
            choices.append ((num, option.content))
            num+=1

        return tuple(choices)

    class Admin:
        pass
    
    class Meta:
	ordering = ['pref_id','id',]      






