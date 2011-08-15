# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm, SplitDateTimeWidget, RadioSelect
#from django.forms.fields import email_re

from django.contrib.auth.models import User
from django.template import Template, Context
import re

from main_test import settings
from main_test.misc import util

import os

from main_test.events.models import *
from main_test.submissions.models import *

alphanumric = re.compile(r"[a-zA-Z0-9]+$")
GENDER_CHOICES = (
        (1, 'Male'),
        (2, 'Female'),
        )
        

HOSPI_CHOICES = (
        (1, 'Yes.'),
        (0, 'No.'),
        )

FILES_WHITELIST = ('.pdf','.txt','.doc','.docx','.zip','.avi','.wmv','.xls','.xlsx','.ppt','.pptx','.rar','.tar','.tar.gz','.dwg',)

class ExtFileField(forms.FileField):
    """
    Same as forms.FileField, but you can specify a file extension whitelist.
    Example usage:
    >>> from django.core.files.uploadedfile import SimpleUploadedFile
    >>>
    >>> t = ExtFileField(ext_whitelist=(".pdf", ".txt"))
    >>>
    >>> t.clean(SimpleUploadedFile('filename.pdf', 'Some File Content'))
    >>> t.clean(SimpleUploadedFile('filename.txt', 'Some File Content'))
    >>>
    >>> t.clean(SimpleUploadedFile('filename.exe', 'Some File Content'))
    Traceback (most recent call last):
    ...
    ValidationError: [u'Not allowed filetype!']
    """
    def __init__(self, *args, **kwargs):
        ext_whitelist = kwargs.pop("ext_whitelist")
        self.ext_whitelist = [i.lower() for i in ext_whitelist]

        super(ExtFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(ExtFileField, self).clean(*args, **kwargs)
        if data is None:
            if self.required:
                raise ValidationError("This file is required")
            else:
                return
        else:        
            filename = data.name
            ext = os.path.splitext(filename)[1]
            ext = ext.lower()
            if ext not in self.ext_whitelist:
                raise forms.ValidationError("Not allowed filetype!")



class AddContactForm(forms.Form):
    option = forms.CharField(max_length=2,help_text='The option the participants will select. Ex: a, b, c, etc.')
    text = forms.CharField(help_text='Type the text for the option here')
    
class EditTabForm(forms.Form):
    title=forms.CharField(required = True, help_text='Title of the tab')
    text=forms.CharField(widget=forms.Textarea(attrs={'id':'myArea2','cols':"80",'rows':"20"}), help_text='Contents of the tab (html content is permitted - For this, first turn rich text formatting OFF)')
    tab_pref=forms.IntegerField(required=True,help_text='A number to help you arrange your tabs. Tabs will be displayed in increasing order of this number')
    
class EditQuestionForm(forms.Form):
    QUESTION_TYPES = (
    ('NORMAL', 'Normal'),
    ('FILE', 'File'),
    ('MCQ', 'MCQ'),
    )
    Q_Number=forms.IntegerField(required=True,help_text='Question number - questions will be displayed in increasing order of question number')
    title=forms.CharField(widget=forms.Textarea, help_text='Type the question here')
    question_type = forms.CharField(max_length=6,widget=forms.Select(choices=QUESTION_TYPES))

class EditQuestionsTabForm(forms.Form):
    title=forms.CharField(help_text='Question tab\'s title (Questions are displayed in a separate tab)')
    tab_pref=forms.IntegerField(required=True,help_text='Where should the question tab be displayed, relative to the other tabs?')
    
class AddFileForm(forms.Form):
    filetitle=forms.CharField(help_text='Title of the file (to be displayed)',required = False)
    tabfile=ExtFileField(ext_whitelist=FILES_WHITELIST,required=False)

class EventForm(ModelForm):
    #start_time = forms.DateTimeField(input_formats=('%d-%m-%y %H:%M',), widget=forms.DateTimeInput(format=('%d-%m-%y %H:%M')), required=False, help_text="Registration start time: DD-MM-YY hh:mm",)
    #end_time = forms.DateTimeField(input_formats=('%d-%m-%y %H:%M',), widget=forms.DateTimeInput(format=('%d-%m-%y %H:%M')), required=False, help_text="Registration end time: DD-MM-YY hh:mm",)
    
    class Meta:
        model = Event
        #fields = ('name', 'registrable', 'questions', 'start_time', 'end_time', 'accommodation', 'logo', 'sponslogo')
        fields = ('display_name', 'menu_image', 'sponslogo','video','registrable','questions')
class EventUpdateForm(forms.Form):
    UpdateContent = forms.CharField(widget=forms.Textarea(), help_text = 'The content of the update, 140 characters or less')

class UpdateSpons(forms.Form):
    text=forms.CharField(widget=forms.Textarea(attrs={'id':'myArea2','cols':"40",'rows':"10"}), help_text='copy and paste the spons image here')

class EventCoresEditPage(forms.Form):
    text=forms.CharField(widget=forms.Textarea(attrs={'id':'myArea2','cols':"150",'rows':"10"}))



class SponsPageForm(forms.Form):
    text=forms.CharField(widget=forms.Textarea(attrs={'id':'myArea2','cols':"150",'rows':"15"}))
    
      

