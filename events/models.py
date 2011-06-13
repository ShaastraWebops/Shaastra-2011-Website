from django.db import models
from django.contrib import admin

from django.contrib.auth.models import User, Group

from main_test.misc.util import camelize
from main_test.settings import *

import os

#Global - Directory where all the other image directories go

#MEDIA_ROOT will be automatically prepended to these when they are used in File/Image Fields
#Assumed MEDIA_ROOT points to /home/shaastra/public_html/2011/media/

def get_eventlogo_path(instance, filename):
	return 'main/events/' + camelize(instance.name) + '/images/eventlogos/' + filename

def get_sponslogo_path(instance, filename):
	return 'main/events/' + camelize(instance.name) + '/images/sponslogos/' + filename

class Event(models.Model):
    name = models.CharField(max_length=80)
    url = models.URLField(null=True,verify_exists=False, blank=True)
    #tags=models.ManyToManyField(Tag, blank=True, null=True)

    # Registration start and end time of the event. 
    start_time = models.DateTimeField(null=True, blank=True, help_text= "Start of registration: YYYY-MM-DD hh:mm" )
    end_time = models.DateTimeField(null=True, blank=True, help_text= "End of registration: YYYY-MM-DD hh:mm" )
    
    # Registration. 
    registrable = models.BooleanField(default=False, help_text= "Can participants register online?")
    questions = models.BooleanField(default=False, help_text= "Will the participant have to answer a questionnaire?")
    #users = models.ManyToManyField(User,  blank=True, null=True, related_name='users_events')
    #chosen_users = models.ManyToManyField(User, blank=True, null=True, related_name='qualified_events')

    # Hospitality.
    accommodation = models.BooleanField(default=False, help_text= "Is accommodation compulsory?")

    # MyShaastra 
    flagged_by = models.ManyToManyField(User,  blank=True, null=True, related_name= 'flagged_events')

    # Logo and Sponsorship logos
    #NOTE: Rename the uploaded image file to event name.
    #NOTE: Assumption: There's one logo and one spons logo for each event
    # Is this the correct path? CHECK THIS!
    logo = models.ImageField(upload_to = get_eventlogo_path, max_length=200, blank = True, null = True)
    sponslogo = models.ImageField(upload_to = get_sponslogo_path, max_length=200, blank = True, null = True)

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
                os.system("mv -T " + MEDIA_ROOT + "main/events/" + camelize(old_instance.name) + " " + MEDIA_ROOT + "main/events/" + camelize(self.name) )
            else:
                print 'entered the else block'
                pass
        except Event.DoesNotExist:
            print 'excepted'
            os.system("mkdir " + MEDIA_ROOT + "main/events/" + camelize(self.name) )
            os.system("mkdir " + MEDIA_ROOT + "main/events/" + camelize(self.name) + "/files")
            os.system("mkdir " + MEDIA_ROOT + "main/events/" + camelize(self.name) + "/submissions")
            os.system("mkdir " + MEDIA_ROOT + "main/events/" + camelize(self.name) + "/images")
            os.system("mkdir " + MEDIA_ROOT + "main/events/" + camelize(self.name) + "/images/eventlogos")
            os.system("mkdir " + MEDIA_ROOT + "main/events/" + camelize(self.name) + "/images/sponslogos")
    	super(Event, self).save(*args, **kwargs) # Call the "real" save() method.
    
    #A directory should not be created every time a new variable is declared
    #Moreover, this completely overrides all else that init is supposed to do
    #def __init__(self, *args, **kwargs):
    #    os.system("mkdir " + MEDIA_ROOT + "main/files/" + camelize(kwargs['name']) )
    #    os.system("mkdir " + MEDIA_ROOT + "main/submissions/" + camelize(kwargs['name']) )
	
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
    
    
    
    # According to sudarshan, tab doesn't contain any images
    #images      = models.ManyToManyField(TabImage      , blank=True, null=True, related_name='questions')
    
    #Sudarshan asked us to separate Q&A from the tabs
    #questions   = models.ManyToManyField(TabQuestion   , blank=True, null=True, related_name='questions')
    #forums      = models.ManyToManyField(TabForum      , blank=True, null=True, related_name='forums')

    def __unicode__(self):
        return self.text
    
    class Meta:
    	ordering = ['pref']
    
    class Admin:
        pass

'''
def get_upload_path(instance, filename):
	return os.path.join('events/', camelize(unicode(instance.Tab.event.name)), '/files/', filename)
'''


class TabFiles(models.Model):
    #File = models.FileField(upload_to=get_upload_path,blank=True,null=True)
    Tab = models.ForeignKey(QuickTabs)
    url = models.URLField(max_length= 500, blank = True , null = True)
    title = models.CharField(max_length = 150, blank = True , null = True )
    
    def delete(self, *args, **kwargs):
        print 'entered the tabfile delete method'
        os.system('rm ' + str(self.url).replace(MEDIA_URL, MEDIA_ROOT) )
        #filename = str(self.url).rsplit('/', 1)[1]   #Already camelized
        #eventname = self.Tab.event.name
        #os.system("rm " + MEDIA_ROOT + "main/events/" + camelize(eventname) + "/files/" + filename)
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
'''
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

class TabForumReply(models.Model):
    reply_by = models.ForeignKey(User,blank=True, null=True, related_name='reply_by')
    #We could display some profile details of the poster. Like in launchpad or bugzilla
    time_stamp = models.DateTimeField(auto_now=False, auto_now_add=False)
    content = models.TextField()
    # Using TextField to allow for long replies, also allows better form handling
    # Id of the TabForumReply object to which the user replied to.
    # Using this we can provide link to the post to which this was a reply. 
    reply_to = models.IntegerField()
    # Number of likes and dislikes for a post. 
    likes = models.IntegerField()
    dislikes = models.IntegerField()
    # NOTE: Do we need edit history? I don't think it's worth implementing this feature.
    
class TabForum(models.Model):
    name = models.CharField( max_length = 30 )
    #Name of the thread , could be decided by the author of the thread
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    #Tags associated with the thread, similar to tags in blogspot/wordpress
    started_by = models.ForeignKey(User,blank=True, null=True, related_name='started_by')
    time_created = models.DateTimeField(auto_now=False, auto_now_add=False)
    time_modified = models.DateTimeField(auto_now=False, auto_now_add=False)
    replies = models.ManyToManyField(TabForumReply,blank=True,null=True,related_name='replies')
    #Reply to each thread , will have user who replied, content and timestamp
    def __str__(self):
        return self.name
    class Admin:
        pass

class QuickTabs(models.Model): 
    # NOTE: Will one text field per tab suffice?
    title  = models.CharField(max_length=80)
    text        = models.CharField(max_length=10000)
    events     = models.ForeignKey(Event)
    #images      = models.ManyToManyField(TabImage      , blank=True, null=True, related_name='questions')
    #questions   = models.ManyToManyField(TabQuestion   , blank=True, null=True, related_name='questions')
    #forums      = models.ManyToManyField(TabForum      , blank=True, null=True, related_name='forums')
  
    def __str__(self):
        return self.text
    class Admin:
        pass



#Team event will be derived from the Event class
#Author: Swaroop Ramaswamy - Inital model 
#Using inheritance instead of foreign key. Seems cleaner 
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

def get_menu_thumbnail_path(instance, filename):
    return 'main/events/images/menu_thumbnails/'

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

