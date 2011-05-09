# have written a very basic crude definition of events_all model




from django.db import models
from django.contrib import admin
from django import forms
from main_test.users.models import *


<<<<<<< HEAD
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
    
=======
class Tag(models.Model):
    name=models.CharField(max_length=30)
    def __str__(self):
        return self.name
    
    class Admin:
        pass


class Event_All(models.Model):
	name  =  models.CharField(max_length=30)
	url   =  models.URLField(verify_exists= True)
	tags  =  models.ManyToManyField(Tag)
	etype =  models.CharField(max_length=30)
	participants  =  models.ManyToManyField(User)
	start_time    =  models.DateTimeField(null= True, blank=True)
	end_time      =  models.DateTimeField(null= True , blank = True)
	coords        =  models.ManyToManyField(User)
	selected_users=  models.ManyToManyField(User)
	#flagged_by   =  models.ManyToManyField()
	is_registrable=  models.BooleanField()
	is_hospi_avail=  models.BooleanField(null=True)
	logo          =  models.ImageField(path="logos/", blank=True, null=True )
    sponslogo     =  models.ImageField(path=" sponslogos/" , blank = True, null =True)
	tabs          =  models.ManyToManyField(Tabs)

	def __str__(self):
		return self.name

	class Admin:
		pass

>>>>>>> 0a813076f395535827c911b8ebd20b542ce8c119
