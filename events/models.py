# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from userportal.registration.models import *
from userportal.misc.util import NORMAL,FILE,MCQ,MESSAGE
from django import forms
from django.db.models import Q
#import forms
class Tag(models.Model):
    name=models.CharField(max_length=30)
    def __str__(self):
        return self.name
    
    class Admin:
        pass

class EventTime(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    #event = models.ForeignKey(Event)

    def __str__(self):
        return "%s to %s"%(str(self.start_time),str(self.end_time))

class Event(models.Model):
    name = models.CharField(max_length=80)
    url = models.URLField(null=True,verify_exists=False, blank=True)
    tags=models.ManyToManyField(Tag, blank=True, null=True)
    #time = models.ManyToManyField(EventTime, blank=True, null=True)
    start_time = models.DateTimeField(null=True,blank=True)
    end_time = models.DateTimeField(null=True,blank=True)
    coords = models.ManyToManyField(User, blank=True, null=True, related_name='coord_events')
    users = models.ManyToManyField(User, related_name='events', blank=True, null=True)
    chosen_users = models.ManyToManyField(User, blank=True, null=True, related_name='qualified_events')
    registerable = models.BooleanField()
    hospi_only=models.BooleanField(default=False)
    logo=models.FileField(upload_to="logos/", blank=True, null=True)
    
    def __str__(self):
        return self.name

    class Admin:
        pass

class EventAdmin(admin.ModelAdmin):
    #filter_vertical = ['users',]
    filter_horizontal = ['coords','chosen_users']
    def queryset(self, request):
	if request.user.is_superuser :
	  return Event.objects.all()
	return Event.objects.filter(coords=request.user)

class TeamEventAdmin(admin.ModelAdmin):
    def queryset(self, request):
	if request.user.is_superuser :
	  return TeamEvent.objects.all()
	return TeamEvent.objects.filter(coords=request.user)

class MessageAdmin(admin.ModelAdmin):
    list_display = ('event','content','type')
    filter_horizontal=['questions']
    fieldsets=(
	(None, {
	    'fields': (),
	    }),
	( None , {
	    'fields': ('content','type','qn_lower','qn_higher'),
	    'description': "The message to be displayed, and its type.<br />In case of 'Specific' type, mention the range of questions for which this message should appear."
	    }),
	 )
	
    def queryset(self, request):
	if request.user.is_superuser:
	    return Message.objects.all()
	curr_event = Event.objects.filter(coords = request.user)
	return Message.objects.filter(event = curr_event[0])
	
    def save_model(self, request, obj, form, change):
	#if not (obj.qn_lower and obj.qn_higher):
	      #raise ValueError("Enter a range please. Fill up the other value.")
	curr_event =  Event.objects.filter(coords=request.user)
        obj.event = curr_event[0]
        obj.save()
    
    def formfield_for_manytomanyfield(self, db_field, request, **kwargs):
        print "heya"
        if db_field.name == "question":
            kwargs["queryset"] = Question.objects.filter(event = Event.objects.filter(coords = request.user)[0])
            return db_field.formfield(**kwargs)
        return super(MyModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

class QuestionAdmin(admin.ModelAdmin):
    #fields = ('content','type','pref_id',)
    ordering = ['pref_id','id',]
    list_display = ('content','pref_id','event')
    fieldsets=(
	(None, {
	    'fields': (),
        }),
        ( None , {
	    'fields': ('content','type','pref_id',),
            'description': "The Prefered Question Number Of this question. Change it to change the order in which the questions appear."
        }),

    )
    def queryset(self, request):
	if request.user.is_superuser :
	  return Question.objects.all()
	curr_event =  Event.objects.filter(coords=request.user)
	return Question.objects.filter(event = curr_event[0])
	
    
    def save_model(self, request, obj, form, change):
	if change:
	    ex_pref_id = Question.objects.get(id=obj.id).pref_id
	    if not obj.pref_id ==  ex_pref_id :
		self.change_pref_id(obj) 
	curr_event =  Event.objects.filter(coords=request.user)
        obj.event = curr_event[0]
        obj.save()
	if not obj.pref_id:
	    obj.pref_id = Question.objects.filter(event = obj.event).count()
	    obj.save()
    
    def change_pref_id (self,obj):
	"""id1 is the prefered id and ex_pref_id is the previous prefered id"""
	ex_pref_id = Question.objects.get(id=obj.id).pref_id
	questions = Question.objects.filter(event = obj.event)
	for qn in questions:
	    if obj.pref_id > ex_pref_id :
		if qn.pref_id > ex_pref_id and qn.pref_id <= obj.pref_id :
		    qn.pref_id = qn.pref_id - 1
	    elif obj.pref_id < ex_pref_id :
		if qn.pref_id < ex_pref_id and qn.pref_id >= obj.pref_id :
		    qn.pref_id = qn.pref_id + 1    
	    qn.save()

class TeamQuestionAdmin(admin.ModelAdmin):
    #fields = ('content','type')
    ordering = ['pref_id','id',]
    list_display = ('content','pref_id','event')
    fieldsets=(
	(None, {
	    'fields': (),
        }),
        ( None , {
	    'fields': ('content','type','pref_id',),
            'description': "The Prefered Question Number Of this question : Change it to change the order in which the questions appear."
        }),

    )    
    def queryset(self, request):
	if request.user.is_superuser :
	  return TeamQuestion.objects.all()
	curr_event =  TeamEvent.objects.filter(coords=request.user)
	return TeamQuestion.objects.filter(event=curr_event[0])

    def save_model(self, request, obj, form, change):
	if change:
	    ex_pref_id = TeamQuestion.objects.get(id=obj.id).pref_id
	    if not obj.pref_id ==  ex_pref_id :
		self.change_pref_id(obj) 
	curr_event =  TeamEvent.objects.filter(coords=request.user)
        obj.event = curr_event[0]
        obj.save()
	if not obj.pref_id:
	    obj.pref_id = TeamQuestion.objects.filter(event = obj.event).count() 
	    obj.save()
	 
    def change_pref_id (self,obj):
	"""id1 is the prefered id and ex_pref_id is the previous prefered id"""
	ex_pref_id = TeamQuestion.objects.get(id=obj.id).pref_id
	questions = TeamQuestion.objects.filter(event = obj.event)
	for qn in questions:
	    if obj.pref_id > ex_pref_id :
		if qn.pref_id > ex_pref_id and qn.pref_id <= obj.pref_id :
		    qn.pref_id = qn.pref_id - 1
	    elif obj.pref_id < ex_pref_id :
		if qn.pref_id < ex_pref_id and qn.pref_id >= obj.pref_id :
		    qn.pref_id = qn.pref_id + 1    
	    qn.save()

class TagAdmin(admin.ModelAdmin):
    def queryset(self, request):
	if request.user.is_superuser :
	  return Tag.objects.all()
	curr_event =  Event.objects.filter(coords=request.user)
	return Tag.objects.filter(event=curr_event)

class TeamMCQOptionAdmin(admin.ModelAdmin):
    def queryset(self, request):
        if request.user.is_superuser :
           return TeamMCQOption.objects.all()
        curr_event =  TeamEvent.objects.filter(coords=request.user)
        questions = TeamQuestion.objects.filter(event=curr_event[0], type=MCQ)
        qset=TeamMCQOption.objects.get_query_set()
        for qsn in questions:
            qset=qset | TeamMCQOption.objects.filter(question=qsn)
        return qset
   
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        print "hey"
        if db_field.name == "question":
            kwargs["queryset"] = TeamQuestion.objects.filter(event = TeamEvent.objects.get(coords = request.user),type=3)
            return db_field.formfield(**kwargs)
        return super(MyModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

class TeamEvent(models.Model):
    name = models.CharField(max_length=80)
    url = models.URLField(null=True,blank=True,verify_exists=False)
    tags=models.ManyToManyField(Tag, blank=True, null=True)
    #time = models.ManyToManyField(EventTime,blank=True,null=True)
    coords = models.ManyToManyField(User, blank=True, null=True, related_name='coord_teamevents')
    teams = models.ManyToManyField(Team, blank=True, null=True, related_name='events')
    chosen_teams = models.ManyToManyField(Team, blank=True, null=True, related_name='qualified_events')
    registerable = models.BooleanField()
    hospi_only=models.BooleanField(default=False)
    start_time = models.DateTimeField(null=True,blank=True)
    end_time = models.DateTimeField(null=True,blank=True)
    logo=models.FileField(upload_to="logos/", blank=True, null=True)
    size = models.SmallIntegerField()
    min_size = models.SmallIntegerField()
    
    def __str__(self):
        return self.name

    class Admin:
        pass

class Question(models.Model):
    TYPE = (
            (1, 'Normal'),
            (2, 'File'),
            (3, 'MCQ'),
            #(4, 'Message'),
            )
    
    event = models.ForeignKey(Event)
    content = models.TextField(max_length=1000)
    pref_id = models.IntegerField(blank= False, null = False ,verbose_name = 'Question Number. Note that this will be the number displayed in the button for this question.',)
    type = models.IntegerField(choices=TYPE)
    visible = models.BooleanField(default=True)
    def __str__(self):
        return self.content
    def get_choices (self):
        if self.type != 3:
            raise ValueError
        list = MCQOption.objects.filter(question=self)
        choices = []
        num = 1
        for option in list:
            choices.append ((num, option.content))
            num+=1

        return tuple(choices)

    class Admin:
        pass
    
    class Meta:
	ordering = ['pref_id','id',]

class TeamQuestion(models.Model):
    TYPE = (
            (1, 'Normal'),
            (2, 'File'),
            (3, 'MCQ'),
            #(4, 'Message'),
            )
    event = models.ForeignKey(TeamEvent)
    content = models.TextField(max_length=1000)
    pref_id = models.IntegerField(blank= True, null = True ,verbose_name = 'Prefered Question Number',)
    type = models.IntegerField(choices=TYPE)
    visible = models.BooleanField(default=True)
    def __str__(self):
        return self.content
    def get_choices (self):
        if self.type != 3:
            raise ValueError
        list = MCQOption.objects.filter(question=self)
        choices = []
        num = 1
        for option in list:
            choices.append ((num, option.content))
            num+=1

        return tuple(choices)

    class Meta:
	ordering = ['pref_id','id',]

    class Admin:
        pass

class Message(models.Model):
    TYPE=(
	  (1,'Overall'),
	  (2,'Specific'),
	  )
    event = models.ForeignKey(Event)
    content = models.TextField(max_length=1000)
    type = models.IntegerField(choices=TYPE)
    visible = models.BooleanField(default=True)
    questions = models.ManyToManyField(Question,related_name = 'questions_msg')
    qn_lower = models.IntegerField(blank=True,null=True,verbose_name="The lower value of the range of questions for which this message should appear")
    qn_higher = models.IntegerField(blank=True,null=True,verbose_name="The higher value of the range of questions for which this message should appear")
    
    def __str__(self):
	return self.content
	
    class Admin:
	pass
    class Meta:
	ordering = ['id',]

class MCQOption(models.Model):
    question = models.ForeignKey(Question)
    content = models.CharField(max_length=255)

    def __str__(self):
        return self.content

    class Admin:
        pass

class MCQOptionAdmin(admin.ModelAdmin):
    def queryset(self, request):
        if request.user.is_superuser :
            return MCQOption.objects.all()
        curr_event =  Event.objects.filter(coords=request.user)
        questions = Question.objects.filter(event=curr_event[0], type=MCQ)
        qset=MCQOption.objects.get_query_set()
        for qsn in questions:
            qset=qset | MCQOption.objects.filter(question=qsn)
        return qset
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        print "hey"
        if db_field.name == "question":
            kwargs["queryset"] = Question.objects.filter(event = Event.objects.filter(coords = request.user)[0],type=3)
            return db_field.formfield(**kwargs)
        return super(MyModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

class TeamMCQOption(models.Model):
    question = models.ForeignKey(TeamQuestion)
    content = models.CharField(max_length=255)

    def __str__(self):
        return self.content
    
    class Admin:
        pass

class Answer(models.Model):
    question = models.ForeignKey(Question, editable=False)
    answered_by = models.ForeignKey(User)
    content = models.TextField(max_length=1000,blank=True,null=True)

    def __str__(self):
        return self.content
        
    class Admin:
        pass

class TeamAnswer(models.Model):
    question = models.ForeignKey(TeamQuestion, editable=False)
    answered_by = models.ForeignKey(Team)
    content = models.TextField(max_length=1000,blank=True,null=True)

    def __str__(self):
        return self.content
        
    class Admin:
        pass

class MCQAnswer (models.Model):
    question = models.ForeignKey(Question, editable=False)
    answered_by = models.ForeignKey(User)
    content = models.ForeignKey(MCQOption)

    def __str__(self):
        return str(self.content)
        
    class Admin:
        pass

class TeamMCQAnswer (models.Model):
    question = models.ForeignKey(TeamQuestion, editable=False)
    answered_by = models.ForeignKey(Team)
    content = models.ForeignKey(TeamMCQOption)

    def __str__(self):
        return str(self.content)
        
    class Admin:
        pass

class FileAnswer(models.Model):
    question = models.ForeignKey(Question, editable=False)
    content=models.FileField(upload_to="files/", null=True)
    answered_by = models.ForeignKey(User)

    def __str__(self):
        return self.content

    class Admin:
        pass

class TeamFileAnswer(models.Model):
    question = models.ForeignKey(TeamQuestion, editable=False)
    answered_by = models.ForeignKey(Team)
    content=models.FileField(upload_to="files/", null=True)

    def __str__(self):
        return self.content

    class Admin:
        pass

class Submission(models.Model):
    user = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    interesting = models.BooleanField(default=False,blank = True)
    sub_read = models.BooleanField(default=False,blank = True)
    selected = models.BooleanField(default=False,blank = True)
    score = models.FloatField(null=True, blank=True)
    rank = models.IntegerField(null=True,blank=True)
    is_new = models.BooleanField(default=True, blank=True)
    modified = models.BooleanField(default=False, blank=True)
    
class TeamSubmission(models.Model):
    team = models.ForeignKey(Team)
    event = models.ForeignKey(TeamEvent)
    interesting = models.BooleanField(default=False,blank = True)
    sub_read = models.BooleanField(default=False,blank = True)
    selected = models.BooleanField(default=False,blank = True)
    score = models.FloatField(null=True, blank=True)
    rank = models.IntegerField(null=True,blank=True)
    is_new = models.BooleanField(default=True, blank=True)
    modified = models.BooleanField(default=False, blank=True)
