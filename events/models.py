

from django.db import models
from django.contrib import admin

from django.contrib.auth.models import User, Group

#Global - Directory where all the other image directories go
IMAGE_DIR = '2011/media/main/images/'
FILE_DIR = '2011/media/main/files/'



class Tag(models.Model):   
#E.g.: aerofest, coding etc
    name=models.CharField(max_length=30)
    def __unicode__(self):
        return self.name
    class Admin:
        pass

class Event(models.Model):
    name = models.CharField(max_length=80)
    url = models.URLField(null=True,verify_exists=False, blank=True)
    tags=models.ManyToManyField(Tag, blank=True, null=True)

    # Registration start and end time
    start_time = models.DateTimeField(null=True,blank=True)
    end_time = models.DateTimeField(null=True,blank=True)
    

    # Registration
    registrable = models.BooleanField(default=False)
    users = models.ManyToManyField(User,  blank=True, null=True, related_name='users_events')
    chosen_users = models.ManyToManyField(User, blank=True, null=True, related_name='qualified_events')

    # Hospitality
    accommodation = models.BooleanField(default=False)

    # MyShaastra 
    flagged_by = models.ManyToManyField(User,  blank=True, null=True, related_name='flagged_events')

    # Logo and Sponsorship logos
    #NOTE: Rename the uploaded image file to event name.
    #NOTE: Assumption: There's one logo and one spons logo for each event
    # Is this the correct path? CHECK THIS!
    logo=models.FileField(upload_to="%sevent_logos/"%IMAGE_DIR, blank=True, null=True)
    sponslogo=models.FileField(upload_to="%sspons_logos/"%IMAGE_DIR, blank=True, null=True)

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
    
    
    # According to sudarshan, tab doesn't contain any images
    #images      = models.ManyToManyField(TabImage      , blank=True, null=True, related_name='questions')
    
    #Sudarshan asked us to separate Q&A from the tabs
    #questions   = models.ManyToManyField(TabQuestion   , blank=True, null=True, related_name='questions')
    #forums      = models.ManyToManyField(TabForum      , blank=True, null=True, related_name='forums')

    def __unicode__(self):
        return self.text
    class Admin:
        pass

class TabFile(models.Model):
    
    file_id = models.AutoField(unique=True, primary_key=True)
    #File = models.FileField(upload_to=('%sTabFile/%s'%(FILE_DIR,file_id)),blank=True, null=True)
    #Pack this file id funda. we ll just upload to file dir. We ll have to give a warning message if they upload a file and that overwrites the file in the directory. This way files wont be arbitrarily named
    #File = models.FileField(upload_to='%sTabFile/'%(FILE_DIR),blank=True, null=True)
    File = models.FileField(upload_to='tab/',blank=True,null=True)
    Tab = models.ForeignKey(QuickTabs)
    filename = models.CharField(max_length= 150)
    title = models.CharField(max_length = 150)
    
    def __unicode__(self):
        return ('%sTabFile/'%(FILE_DIR) + self.filename )
    class Admin:
        pass

class TabImage(models.Model):
    # TASK: Each tab can have more than one image. Each tab can be associated with more than one TabImage object(s)
    # Rename the image file to the id of the TabImage object. 
    # Ex: When a user wants to upload a image file, a TabImage object is created. Say it's id is 44. 
    # Then rename the file to 44.jpg and store it in "public_html/2011/TabImage/"
    image_id = models.AutoField(unique=True, primary_key=True)
    image = models.ImageField(upload_to=('%sTabImage/%s'%(IMAGE_DIR,image_id)),blank=True, null=True)
    # I really don't know whether this will work. Just change this if you find out a method that works 
    # Converted image_id to a string and then changed the upload_to path.  
    # Unique image id, the idea is to rename the file to the image_id
    # We can identify each image by it's unique image_ids
    def __unicode__(self):
        return str(self.image_id)
    class Admin:
        pass

#Team event will be derived from the Event class
#Author: Swaroop Ramaswamy - Inital model 
#Using inheritance instead of foreign key. Seems cleaner 
'''      
class TeamEvent(Event):

    teams = models.ManyToManyField(Team,  blank=True, null=True, related_name='Team_events')
    chosen_teams = models.ManyToManyField(Team, blank=True, null=True, related_name='Team_qualified_events')

    def __unicode__(self):
        return self.name
    #I m not sure if I can use foreign keys this way. Somebody please check this.   
    # karthikabinav here:
    # checked the above way and is a correct way to do it.
    # reference:http://svn.tools.ietf.org/svn/tools/ietfdb/branch/idsubmit/ietf/idtracker/models.py
    # in the above reference he uses the above way for foriegn keys     
    class Admin:
        pass    
'''

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






