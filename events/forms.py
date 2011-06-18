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

class CoordsLoginForm(forms.Form):
    username=forms.CharField(help_text='The coord username given to you')
    password=forms.CharField(widget=forms.PasswordInput, help_text='The coord password given to you')


class AddContactForm(forms.Form):
    option = forms.CharField(max_length=2,help_text='The option the participants will select. Ex: a, b, etc.')
    text = forms.CharField(help_text='Description of the option.')
    
class EditTabForm(forms.Form):
    title=forms.CharField(help_text='Title of the tab')
    text=forms.CharField(widget=forms.Textarea(attrs={'id':'myArea2'}), help_text='Text content of the tab')
    tab_pref=forms.IntegerField(required=True,help_text='Order of the tab for displaying.')
    
class EditQuestionForm(forms.Form):
    QUESTION_TYPES = (
    ('NORMAL', 'Normal'),
    ('FILE', 'File'),
    ('MCQ', 'MCQ'),
    )
    Q_Number=forms.IntegerField(required=True,help_text='Question number')
    title=forms.CharField(widget=forms.Textarea, help_text='The description of the question.')
    question_type = forms.CharField(max_length=6,widget=forms.Select(choices=QUESTION_TYPES))
    
class AddFileForm(forms.Form):
    filetitle=forms.CharField(help_text='Title of the file',required = False)
    tabfile=ExtFileField(ext_whitelist=FILES_WHITELIST,required=False)

class EventForm(ModelForm):
    #start_time = forms.DateTimeField(input_formats=('%d-%m-%y %H:%M',), widget=forms.DateTimeInput(format=('%d-%m-%y %H:%M')), required=False, help_text="Registration start time: DD-MM-YY hh:mm",)
    #end_time = forms.DateTimeField(input_formats=('%d-%m-%y %H:%M',), widget=forms.DateTimeInput(format=('%d-%m-%y %H:%M')), required=False, help_text="Registration end time: DD-MM-YY hh:mm",)
    class Meta:
        model = Event
        #fields = ('name', 'registrable', 'questions', 'start_time', 'end_time', 'accommodation', 'logo', 'sponslogo')
        fields = ('name', 'logo', 'sponslogo')
