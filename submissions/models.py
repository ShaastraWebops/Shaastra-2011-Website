from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User, Group
from main_test.events.models import *
from main_test.users.models import UserProfile, Team


class BaseSubmission(models.Model):
    event = models.ForeignKey(Event,null=False)
    # Additional features. 
    submitted = models.BooleanField()
    interesting = models.BooleanField(default=False,blank = True)
    sub_read = models.BooleanField(default=False,blank = True)
    selected = models.BooleanField(default=False,blank = True)
    score = models.FloatField(null=True, blank=True)
    rank = models.IntegerField(null=True,blank=True)
    is_new = models.BooleanField(default=True, blank=True)
    modified = models.BooleanField(default=False, blank=True)
    
    def render(self):
        pass
    class Admin:
        pass
    class Meta:
        ordering = ['id']


class IndividualSubmissions(BaseSubmission):
    participant = models.ForeignKey(UserProfile)
    
    def render(self):
        pass
    class Admin:
        pass
    class Meta:
        ordering = ['id']
    
class TeamSubmission(BaseSubmission):
    team = models.ForeignKey(Team)
    
    def render(self):
        pass
    class Admin:
        pass
    class Meta:
        ordering = ['id']


class Answer(models.Model):
    question = models.ForeignKey(Question)
    submission = models.ForeignKey(BaseSubmission)
    
    def render(self):
        pass
    class Admin:
        pass
    class Meta:
        ordering = ['id',]
    
class Answer_Text(Answer):
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

def get_upload_path(instance, filename):
    event = instance.question.event
    return "events/" + camelize(event.name) + "/submissions/" + filename
    
class Answer_file(Answer):    
    File = models.FileField(upload_to = get_upload_path, max_length = 200, blank = True, null = True)
    def render(self):
        return self.File.name
    def __unicode__(self):
        return self.File.url
    class Admin:
        pass
