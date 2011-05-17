# Inheritance is COMPLETELY screwed up. Need to fix ALL team events etc. 
# Please see http://docs.djangoproject.com/en/dev/topics/db/models/ . Esp the last para.
# NEEDS FIXING IMMEDIATELY


from django.db import models
from django.contrib import admin

from django.contrib.auth.models import User, Group
from users.models import Team

# Please note that __str__ is not recommended in django docs. Should we switch to unicode ?
class Tag(models.Model):   
#E.g.: aerofest, coding etc
    name=models.CharField(max_length=30)
    def __str__(self):
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
    coords = models.ForeignKey(User)

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
    logo=models.FileField(upload_to="public_html/2011/events_logos/", blank=True, null=True)
    sponslogo=models.FileField(upload_to="public_html/2011/events_sponslogos/", blank=True, null=True)

    def __str__(self):
        return self.name

    class Admin:
        pass  

class QuickTabs(models.Model): 
    # NOTE: Will one text field per tab suffice?

    title       = models.CharField(max_length=100)
    event       = models.ForeignKey(Event)
    text        = models.TextField() 

    #images      = models.ManyToManyField(TabImage      , blank=True, null=True, related_name='questions')
    #questions   = models.ManyToManyField(TabQuestion   , blank=True, null=True, related_name='questions')
    #forums      = models.ManyToManyField(TabForum      , blank=True, null=True, related_name='forums')

    def __str__(self):
        return self.text
    class Admin:
        pass



class TabImage(models.Model):
    # TASK: Each tab can have more than one image. Each tab can be associated with more than one TabImage object(s)
    # Rename the image file to the id of the TabImage object. 
    # Ex: When a user wants to upload a image file, a TabImage object is created. Say it's id is 44. 
    # Then rename the file to 44.jpg and store it in "public_html/2011/TabImage/"
    image_id = models.AutoField(unique=True, primary_key=True)
    image = models.ImageField(upload_to=('public_html/2011/TabImage/%s.jpg',str(image_id)))
    # I really don't know whether this will work. Just change this if you find out a method that works 
    # Converted image_id to a string and then changed the upload_to path.  
    # Unique image id, the idea is to rename the file to the image_id
    # We can identify each image by it's unique image_ids
    def __str__(self):
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

#Team event will be derived from the Event class
#Author: Swaroop Ramaswamy - Inital model 
#Using inheritance instead of foreign key. Seems cleaner       
class TeamEvent(Event):

    teams = models.ManyToManyField(Team,  blank=True, null=True, related_name='Team_events')
    chosen_teams = models.ManyToManyField(Team, blank=True, null=True, related_name='Team_qualified_events')

    def __str__(self):
        return self.name
    #I m not sure if I can use foreign keys this way. Somebody please check this.   
    # karthikabinav here:
    # checked the above way and is a correct way to do it.
    # reference:http://svn.tools.ietf.org/svn/tools/ietfdb/branch/idsubmit/ietf/idtracker/models.py
    # in the above reference he uses the above way for foriegn keys     
    class Admin:
        pass    

#Author: Praveen Venkatesh
QUESTION_TYPE = ((1, 'Text'),
                 (2, 'File'),
                 (3, 'MCQ'),)



#Author: Praveen Venkatesh - Created inital model

#Author: Praveen Venkatesh - Created inital model
#Try to use ModelForms in order to render this model - appears to make things easy		
#Instead of derived classes, now using abstract class
class Question_base(models.Model):

    #Question specifics
    text = models.TextField(max_length = 1000, blank = True, null = True)
    question_type = models.IntegerField(choices = QUESTION_TYPE, blank = False, null = False)
    question_number = models.IntegerField ( blank = False, null = False, verbose_name = 'Number displayed in the button for this question.',) 

    #File specifics
    question_file = models.FileField(upload_to = ('files/%s/',str(Event)), blank = True, null = True)
	#Not sure if this syntax is correct             ^^^^^
    #Should we do this or should be do what we did for Tabimage ?    
    #Retrieve choices in case of MCQ type
    def get_choices(self):
        if(self.question_type != 3):
            raise ValueError
        list = MCQOption.objects.filter(question_id = self)   
        choices = []
        num = 1
        for option in list:
            choices.append( (num, option.choice_text) )
            num += 1
        return tuple(choices)

    #To render or not to render
    visible = models.BooleanField(default = True)

    #Define thyself!
    def __str__(self):
        return self.text
    #Should we have a question id ? Returning the text field doesn't seem so appropriate to me. We can have question id as an AutoField and return str(self.question_id)    

    class Admin:
        pass

    class Meta:
        ordering = ['question_number', 'id',]
        abstract = True


class Question(Question_base):
    #Event specifics
    event = models.ForeignKey(Event)

class TeamQuestion(Question_base):
    event=models.ForeignKey(TeamEvent)

class MCQOption(models.Model):

    #Question specifics
    question_id = models.ForeignKey(Question)

    #Choice specifics
    choice_text = models.TextField(max_length = 1000)

    def __str__(self):
        return self.choice_text

    class Admin:
        pass

    class Meta:
        ordering = ['id',]

class TeamMCQOption(MCQOption):
    #question_id = models.ForeignKey(TeamQuestion)
    pass		 


#Author: Sivaramakrishnan, created the initial model
#This is has been changed using abstract classes.
class Submission_base(models.Model):


    interesting = models.BooleanField(default=False,blank = True)
    sub_read = models.BooleanField(default=False,blank = True)
    selected = models.BooleanField(default=False,blank = True)
    score = models.FloatField(null=True, blank=True)
    rank = models.IntegerField(null=True,blank=True)
    is_new = models.BooleanField(default=True, blank=True)
    modified = models.BooleanField(default=False, blank=True)

    class meta:
        abstract = True


class TeamSubmission(Submission_base):

    team = models.ManyToManyField(Team)
    event = models.ManyToManyField(TeamEvent)

class Submission(Submission_base):

    user = models.ManyToManyField(User)
    event = models.ManyToManyField(Event)

class MCQAnswer_base (models.Model):

    content = models.ForeignKey(MCQOption)

    def __str__(self):
        return str(self.content)

    class Admin:
        pass

    class meta:
        abstract=True	
class MCQAnswer(MCQAnswer_base):
    question = models.ForeignKey(Question, editable=False)	
    answered_by = models.ForeignKey(User)

class TeamMCQAnswer (MCQAnswer_base):
    question = models.ForeignKey(TeamQuestion, editable=False)
    answered_by = models.ForeignKey(Team)

class FileAnswer_base(models.Model):

    content=models.FileField(upload_to="files/", null=True)

    def __str__(self):
        return self.content

    class Admin:
        pass

    class meta:
        abstract=True	

class FileAnswer(FileAnswer_base):
    question = models.ForeignKey(Question, editable=False)      
    answered_by = models.ForeignKey(User)


class TeamFileAnswer(FileAnswer_base):
    question = models.ForeignKey(TeamQuestion, editable=False)    
    answered_by = models.ForeignKey(Team)





