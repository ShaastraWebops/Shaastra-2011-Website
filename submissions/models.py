from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User, Group
from main_test.events.models import *

'''
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
    def __unicode__(self):
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
'''
'''
class Question(models.Model):
    
    QUESTION_TYPE = (
    (1, 'Normal'),
    (2, 'File'),
    (3, 'MCQ'),
    )
    
    which_event = models.ForeignKey(Event)
    question_number = models.IntegerField (blank = False, null = False, verbose_name = 'Number displayed in the button for this question.',) 
    instructions = models.TextField(blank = True, null = True)
    question_type = models.IntegerField(choices = QUESTION_TYPE, blank = False, null = False)
    
    def __unicode__(self):
        return self.instructions
    
    class Admin:
        pass
    
    class Meta:
        ordering = ['question_number']
   '''     
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
        ordering = ['option',]
        
'''

class Submission(models.Model):
    participant = models.ForeignKey(User, related_name='team_leaders')
    team = models.ManyToManyField(User, null=True, blank = True, related_name='team_members')
    
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

class Answer_text(Answer):
    
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
    return "main/events/" + camelize(event.name) + "/submissions/" + filename

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

''

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
