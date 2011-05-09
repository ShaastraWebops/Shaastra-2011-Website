from django.db import models
from django.contrib import admin
from main_test.users import *



# Author: Chetan Bademi - Wrote the initial model
class Tag(models.Model):   
#E.g.: aerofest, coding etc
    name=models.CharField(max_length=30)
    def __str__(self):
        return self.name
    class Admin:
        pass
    
# Author: Chetan Bademi - Wrote the initial model
class Event(models.Model):
    name = models.CharField(max_length=80)
    url = models.URLField(null=True,verify_exists=False, blank=True)
    tags=models.ManyToManyField(Tag, blank=True, null=True)
    
    # Registration start and end time
    start_time = models.DateTimeField(null=True,blank=True)
    end_time = models.DateTimeField(null=True,blank=True)
    coords = models.ManyToManyField(generic_user, blank=True, null=True, related_name='coord_events')
    
    # Registration
    registrable = models.BooleanField(default=False)
    users = models.ManyToManyField(generic_user,  blank=True, null=True, related_name='users_events')
    chosen_users = models.ManyToManyField(generic_user, blank=True, null=True, related_name='qualified_events')
    
    # Hospitality
    accommodation = models.BooleanField(default=False)
    
    # MyShaastra 
    flagged_by = models.ManyToManyField(generic_user,  blank=True, null=True, related_name='flagged_events')
    
    # Logo and Sponsorship logos
    #NOTE: Rename the uploaded image file to event name.
    #NOTE: Assumption: There's one logo and one spons logo for each event
    # Is this the correct path? CHECK THIS!
    logo=models.FileField(upload_to="public_html/2011/events_logos/", blank=True, null=True)
    sponslogo=models.FileField(upload_to="public_html/2011/events_sponslogos/", blank=True, null=True)
    
    # Tabs
    tabs = models.ManyToManyField(Tabs, blank=True, null=True, related_name='tabs')
  
    def __str__(self):
        return self.name
        
    class Admin:
        pass



# Author: Chetan Bademi - Wrote the initial model
class Tabs(models.Model): 
    # NOTE: Will one text field per tab suffice?
    text        = models.CharField(max_length=10000)
    images      = models.ManyToManyField(TabImage      , blank=True, null=True, related_name='questions')
    questions   = models.ManyToManyField(TabQuestion   , blank=True, null=True, related_name='questions')
    forums      = models.ManyToManyField(TabForum      , blank=True, null=True, related_name='forums')
  
    def __str__(self):
        return self.name
    class Admin:
        pass



# Author: Chetan Bademi - Wrote the initial model
class TabImage(models.Model):
    # TASK: Each tab can have more than one image. Each tab can be associated with more than one TabImage object(s)
    # Rename the image file to the id of the TabImage object. 
    # Ex: When a user wants to upload a image file, a TabImage object is created. Say it's id is 44. 
    # Then rename the file to 44.jpg and store it in "public_html/2011/TabImage/"
    image_id = models.AutoField(unique=True)
    image = models.ImageField(upload_to=('public_html/2011/TabImage/%s.jpg',str(image_id)))
    # I really don't know whether this will work. Just change this if you find out a method that works 
    # Converted image_id to a string and then changed the upload_to path.  
    # Unique image id, the idea is to rename the file to the image_id
    # We can identify each image by it's unique image_ids
    def __str__(self):
        return self.name
    class Admin:
        pass
    

# Author: Chetan Bademi - Wrote the initial model
class TabForum(models.Model):
    name = models.CharField( max_length = 30 )
    #Name of the thread , could be decided by the author of the thread
    tags = models.ManyToManyField(Tag, blank=True, null=True)
<<<<<<< HEAD
    #Tags associated with the thread, similar to tags in blogspot/wordpress
=======
>>>>>>> 70c37b4c296877cd132f2d270ee62e475795f779
    started_by = models.ForeignKey(generic_user,blank=True, null=True, related_name='started_by')
    time_created = models.DateTimeField(auto_now=False, auto_now_add=False)
    time_modified = models.DateTimeField(auto_now=False, auto_now_add=False)
    replies = models.ManyToManyField(TabForumReply,blank=True,null=True,related_name='replies')
    #Reply to each thread , will have user who replied, content and timestamp
    def __str__(self):
        return self.name
    class Admin:
        pass


# Author: Chetan Bademi - Wrote the initial model
class TabForumReply(models.Model):
    reply_by = models.ForeignKey(generic_user,blank=True, null=True, related_name='reply_by')
<<<<<<< HEAD
    #We could display some profile details of the poster. Like in launchpad or bugzilla
=======
>>>>>>> 70c37b4c296877cd132f2d270ee62e475795f779
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
