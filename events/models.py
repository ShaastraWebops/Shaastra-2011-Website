from django.db import models
from django.contrib import admin

from django.contrib.auth.models import User, Group

from main_test.misc.util import camelize
from main_test.settings import *

import os

SHAASTRA_TEASER_URL = "YH-frgafQuU"

def get_eventlogo_path(instance, filename):
	return 'events/' + camelize(instance.name) + '/images/eventlogos/' + filename

def get_sponslogo_path(instance, filename):
	return 'events/' + camelize(instance.name) + '/images/sponslogos/' + filename

class Event(models.Model):
    name = models.CharField(max_length=80, help_text="Name of event - as it is to be displayed")
    url = models.URLField(null=True,verify_exists=False, blank=True)
    #tags=models.ManyToManyField(Tag, blank=True, null=True)

    # Registration start and end time of the event. 
    start_time = models.DateTimeField(null=True, blank=True, help_text= "Start of registration: YYYY-MM-DD hh:mm" )
    end_time = models.DateTimeField(null=True, blank=True, help_text= "End of registration: YYYY-MM-DD hh:mm" )
    
    # Registration. 
    registrable = models.BooleanField(default=False, help_text= "Can participants register online?")
    questions = models.BooleanField(default=False, help_text= "Will the participant have to answer a questionnaire?")
    team_event = models.BooleanField(default=False, help_text= "Is this a team event?")

    # Hospitality.
    accommodation = models.BooleanField(default=False, help_text= "Is accommodation compulsory?")

    # MyShaastra 
    flagged_by = models.ManyToManyField(User,  blank=True, null=True, related_name= 'flagged_events')

    # Logo and Sponsorship logos
    sponslogo = models.ImageField(upload_to = get_sponslogo_path, max_length=200, blank = True, null = True)
    video = models.URLField(null=True,verify_exists=False,default = SHAASTRA_TEASER_URL )
    def __unicode__(self):
        return self.name
    
    #A directory should only be created when a new event is saved to the db
    def save(self, *args, **kwargs):
        try:
            print 'tried'
            old_instance = Event.objects.get(id = self.id)
            print 'get succeeded'
            #This line raises an exception if old_instance does not exist 
            if old_instance.name != self.name:
                print 'entered the if block'
                os.system("mv " + MEDIA_ROOT + "events/" + camelize(old_instance.name) + " " + MEDIA_ROOT + "events/" + camelize(self.name) )
            else:
                print 'entered the else block'
                pass
        except Event.DoesNotExist:
            print 'excepted'
            os.system("mkdir " + MEDIA_ROOT + "events/" + camelize(self.name) )
            os.system("mkdir " + MEDIA_ROOT + "events/" + camelize(self.name) + "/files")
            os.system("mkdir " + MEDIA_ROOT + "events/" + camelize(self.name) + "/submissions")
            os.system("mkdir " + MEDIA_ROOT + "events/" + camelize(self.name) + "/images")
            os.system("mkdir " + MEDIA_ROOT + "events/" + camelize(self.name) + "/images/eventlogos")
            os.system("mkdir " + MEDIA_ROOT + "events/" + camelize(self.name) + "/images/sponslogos")
    	return super(Event, self).save(*args, **kwargs) # Call the "real" save() method.
    	
    class Admin:
        pass  

class Tag(models.Model):   
#E.g.: aerofest, coding etc
    name = models.CharField(max_length = 30)
    events = models.ManyToManyField(Event)
    def __unicode__(self):
        return self.name
    class Admin:
        pass


class QuickTabs(models.Model): 

    title       = models.CharField(max_length=100)
    event       = models.ForeignKey(Event)
    
    #10kb should be enough.
    text        = models.TextField()
    
    # No more than 10 tabs per event.
    pref = models.IntegerField(max_length=2);
    question_tab = models.BooleanField(default=False)

    def __unicode__(self):
        return self.text
    
    class Meta:
    	ordering = ['pref']
    
    class Admin:
        pass

class TabFiles(models.Model):
    Tab = models.ForeignKey(QuickTabs)
    url = models.URLField(max_length= 500, blank = True , null = True)
    title = models.CharField(max_length = 150, blank = True , null = True )
    
    def delete(self, *args, **kwargs):
        print 'entered the tabfile delete method'
        os.system('rm ' + str(self.url).replace(MEDIA_URL, MEDIA_ROOT) )
        super(TabFiles, self).delete(*args, **kwargs)
    
    def __unicode__(self):
        return self.url
    
    class Admin:
        pass


class Question(models.Model):
    #Tab=models.ForeignKey(QuickTabs)
    Q_Number = models.IntegerField(max_length=2) 
    title=models.CharField(max_length=1500, blank = True , null = True )
    event= models.ForeignKey(Event)
    question_type = models.CharField(max_length=1500, blank = True , null = True )
    def __unicode__(self):
        return self.title
    class Meta:
        ordering = ['Q_Number']
    class Admin:
        pass
    
class MCQ_option(models.Model):
    #Question specifics
    question = models.ForeignKey(Question)
    
    #Choice specifics
    option = models.CharField(max_length = 10)
    text = models.TextField(max_length = 1000)
    
    def __unicode__(self):
        return self.text
        
    class Admin:
        pass
    
    class Meta:
        ordering = ['option']

class Update(models.Model):
	event = models.ForeignKey(Event)
	update_time = models.DateTimeField(null = False)
	
	#Allotting 1kB of space just in case there's a lot of formatting
	#This field should contain an html-ready update for direct display
	content_formatted = models.CharField(max_length = 1000)
	
	def __unicode__(self):
		return self.content
		
	class Admin:
		pass	

def get_menu_thumbnail_path(instance, filename):
    return 'events/images/menu_thumbnails/'

class Menu(models.Model):
    text = models.CharField(max_length = 30, blank = False, null = False)
    order = models.IntegerField(blank = False, null = False)
    parent_menu = models.ForeignKey('self', blank = True, null = True)
    event = models.ForeignKey(Event, blank = True, null = True)
    thumbnail = models.ImageField(upload_to = get_menu_thumbnail_path, blank = True, null = True)
    
    def __unicode__(self):
        return self.text
    
    class Meta:
        ordering = ['order', 'id',]
    
    class Admin:
        pass

