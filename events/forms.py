# -*- coding: utf-8 -*-
from django import forms
from django.db import models as d_models
#from django.core.validators import alnum_re
from django.contrib.auth.models import User
from django.template import Template, Context

from main_test import settings
from main_test.misc import util

from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
import os

from main_test.events.models import *
from main_test.submissions.models import *

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
        filename = data.name
        ext = os.path.splitext(filename)[1]
        ext = ext.lower()
        if ext not in self.ext_whitelist:
	    error_text = 'Not allowed filetype!'
            raise forms.ValidationError(error_text)

class CoordsLoginForm(forms.FormField):
    username=forms.CharField(help_text='The coord username given to you')
    password=forms.CharField(widget=forms.PasswordInput, help_text='The coord password given to you')

class EditTabForm(forms.FormField):
    title=forms.CharField(help_text='Title of the tab')
    text=forms.TextField(widget=forms.TextArea, help_text='Text content of the tab')
    filetitle=forms.CharField(help_text='Title of the file')
    tabfile=forms.ExtFileField(required=False)    
    tab_pref=forms.IntegerField(required=True,help_text='Order of the tab for displaying.')





