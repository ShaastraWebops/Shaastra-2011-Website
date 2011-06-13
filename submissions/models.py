from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User, Group
from main_test.events.models import *

        

class Submission(models.Model):
    participant = models.ForeignKey(User)
    submitted = models.BooleanField()
    question = models.ForeignKey(Question)
    
class TextAnswer(models.Model):
    text = models.TextField(blank = True, null = True)
    def render(self):
        return unicode(self)
    def __unicode__(self):
        return self.text    
    class Admin:
        pass
    
class Answer_MCQ(Answer):
    choice = models.ForeignKey(MCQ_option, blank = True, null = True)
    def render(self):
        return choice.option + " " + choice.text
    def __unicode__(self):
        return choice.text
    class Admin:
        pass
    
    '''
# Will this work? I'm not sure at all. It didn't work for events. 
#def get_upload_path(instance, filename):
    #event = instance.question.event
    #return "main/events/" + camelize(event.name) + "/submissions/" + filename
    
class Answer_file(Answer):    
    File = models.FileField(upload_to = get_upload_path, max_length = 200, blank = True, null = True)
    def render(self):
        return self.File.name
    def __unicode__(self):
        return self.File.url
    class Admin:
        pass
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

    class Meta:
        abstract = True


class TeamSubmission(Submission_base):

    team = models.ManyToManyField(Team)
    event = models.ManyToManyField(TeamEvent)


class Submission(Submission_base):

    user = models.ManyToManyField(User)
    event = models.ManyToManyField(Event)

class MCQAnswer_base (models.Model):

    content = models.ForeignKey(MCQOption)

    def __unicode__(self):
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

    def __unicode__(self):
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
'''
