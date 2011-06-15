from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User, Group
from main_test.events.models import *


class Submission(models.Model):
    participant = models.ForeignKey(User)
    submitted = models.BooleanField()
    #Additional features. 
    interesting = models.BooleanField(default=False,blank = True)
    sub_read = models.BooleanField(default=False,blank = True)
    selected = models.BooleanField(default=False,blank = True)
    score = models.FloatField(null=True, blank=True)
    rank = models.IntegerField(null=True,blank=True)
    is_new = models.BooleanField(default=True, blank=True)
    modified = models.BooleanField(default=False, blank=True)
    
class Answer(models.Model):
    question = models.ForeignKey(Question)
    submission = models.ForeignKey(Submission)
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


#Will this work? I'm not sure at all. It didn't work for events. 
# Yes!!! It does work! Check out how image and spons logos were done!!!
'''
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
'''
