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

class SelectUserForm(forms.Form):
    shaastra_id=forms.CharField()
    user_email = forms.EmailField()

class SubForm(forms.ModelForm):
    #sub_read = forms.BooleanField(label = 'Already Read')
    score = forms.FloatField(max_value=10,min_value=0)
    class Meta:
        model = models.Submission
        exclude = ('user','event','sub_read','is_new','modified')

class SubTForm(forms.ModelForm):
    #sub_read = forms.BooleanField(label = 'Already Read')
    score = forms.FloatField(max_value=10,min_value=0)
    class Meta:
        model = models.TeamSubmission
        exclude = ('team','event','sub_read','is_new','modified')


class AnswerForm (forms.ModelForm):
    question = models.Question()
    content = forms.CharField (max_length=600, widget=forms.Textarea(attrs={'wrap':'physical', 'cols':'75', 'rows':'6'}),required=False)
    msg_present = False
    valuate = SubForm()
    class Meta:
        model = models.Answer
        exclude = ('answered_by', 'question')
    def save (self):
        self.instance.question = self.question
        super(forms.ModelForm, self).save()
    def __init__ (self, user, question, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args,**kwargs)
        self.question = question
        self.instance.answered_by = user
        
class FileAnswerForm (forms.ModelForm):
    question = models.Question()
    content = forms.FileField (required=False)
    msg_present = False
    
    class Meta:
        model = models.FileAnswer
        exclude = ('answered_by', 'question')
    def save (self):
        self.instance.question = self.question
        super(forms.ModelForm, self).save()
    def __init__ (self, user, question, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args,**kwargs)
        self.question = question
        self.instance.answered_by = user
        
    def clean_content(self):
	t= ExtFileField(ext_whitelist = FILES_WHITELIST)
	if self.prefix:
            field_name = '%s-content'%self.prefix
        else:
            field_name = 'content'

        if not self.files.has_key(field_name):
            return
        file_field = self.files[field_name]
        t.clean(file_field)	#throws exception if file type is not matched.
        if file_field._size > settings.MAX_UPLOAD_SIZE:
	  raise forms.ValidationError(_('Please keep filesize under %s. Current filesize is %s') % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(file_field._size)))

        fname=file_field.name
        extn=fname[(fname.rfind('.')+1):]
	print extn
        fname = "%s/files/%s-%d-%d.%s"%(settings.MEDIA_ROOT, util.camelize(self.question.event.name), self.instance.answered_by.id, self.instance.question.id, extn)
        file_field.name = fname

        if os.path.isfile(fname):
            os.remove(fname)

        # Django takes care of saving the file
        return file_field

class MCQAnswerForm(forms.ModelForm):
    question = models.Question ()
    content = forms.ModelChoiceField (queryset=models.MCQOption.objects.all(), widget=forms.RadioSelect(attrs={'class':"output"}), empty_label=None)
    msg_present = False
    class Meta:
        model = models.MCQAnswer
        exclude = ('answered_by', 'question')
    def save (self):
        self.instance.question = self.question
        super(forms.ModelForm, self).save()
    def __init__ (self, user, question, *args, **kwargs):
        self.question = question
        self.content = forms.ModelChoiceField (queryset=models.MCQOption.objects.filter(question=self.question), widget=forms.RadioSelect)
        super(forms.ModelForm, self).__init__(*args,**kwargs)
        self.instance.answered_by = user
        
# "Redundant" form to keep the semantics of other forms
#class MessageForm(forms.Form):
    #question = models.Question ()

    #def __init__ (self, user, question, *args, **kwargs):
        #self.question = question
        #super(forms.Form, self).__init__(*args,**kwargs)
    ## Empty save function to meld with the other question forms
    #def save(self):
        #pass

class TeamAnswerForm (forms.ModelForm):
    question = models.TeamQuestion()
    content = forms.CharField (max_length=600, widget=forms.Textarea(attrs={'wrap':'physical', 'cols':'60', 'rows':'6'}),required=False)
    class Meta:
        model = models.TeamAnswer
        exclude = ('answered_by', 'question')
    def save (self):
        self.instance.question = self.question
        super(forms.ModelForm, self).save()
    def __init__ (self, team, question, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args,**kwargs)
        self.question = question
        self.instance.question = question
        self.instance.answered_by = team

class TeamFileAnswerForm (forms.ModelForm):
    question = models.TeamQuestion()
    content = forms.FileField (required=False)
    
    class Meta:
        model = models.TeamFileAnswer
        exclude = ('answered_by', 'question')
    def save (self):
        self.instance.question = self.question
        super(forms.ModelForm, self).save()
    def __init__ (self, team, question, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args,**kwargs)
        self.question = question
        self.instance.question = question
        self.instance.answered_by = team        

    def clean_content(self):
	t= ExtFileField(ext_whitelist = FILES_WHITELIST)
        if self.prefix:
            field_name = '%s-content'%self.prefix
        else:
            field_name = 'content'

        if not self.files.has_key(field_name):
            return
        file_field = self.files[field_name]
        t.clean(file_field)
        if file_field._size > settings.MAX_UPLOAD_SIZE:
	  raise forms.ValidationError(_('Please keep filesize under %s. Current filesize is %s') % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(file_field._size)))
        fname=file_field.name
        extn=fname[(fname.rfind('.')+1):]
	print extn
        fname = "%s/files/%s-%d-%d.%s"%(settings.MEDIA_ROOT, util.camelize(self.question.event.name), self.instance.answered_by.id, self.instance.question.id, extn)
        file_field.name = fname

        if os.path.isfile(fname):
            os.remove(fname)

        # Django takes care of saving the file
        return file_field

class TeamMCQAnswerForm (forms.ModelForm):
    question = models.TeamQuestion()
    content = forms.ModelChoiceField (queryset=models.TeamMCQOption.objects.all(), widget=forms.RadioSelect(attrs={'class':"output"}), empty_label=None)
    
    class Meta:
        model = models.TeamMCQAnswer
        exclude = ('answered_by', 'question')
    def save (self):
        self.instance.question = self.question
        super(forms.ModelForm, self).save()
    def __init__ (self, team, question, *args, **kwargs):
        self.question = question
        self.queryset= models.TeamMCQOption.objects.filter(question=self.question)
        self.content = forms.ModelChoiceField (queryset=models.TeamMCQOption.objects.filter(question=self.question), widget=forms.RadioSelect)
        super(forms.ModelForm, self).__init__(*args,**kwargs)
        # The below code was found on Django Code Snippets where to filter the Queryset of the form something like this needs to be done!
        #I don't know why ... http://www.djangosnippets.org/snippets/625/
        if self.instance:
            self.fields['content'].queryset = models.TeamMCQOption.objects.filter(question=question)
        print self.queryset
        self.instance.answered_by = team

# "Redundant" form to keep the semantics of other forms
class TeamMessageForm(forms.Form):
    question = models.TeamQuestion ()

    def __init__ (self, user, question, *args, **kwargs):
        self.question = question
        super(forms.Form, self).__init__(*args,**kwargs)
    # Empty save function to meld with the other question forms
    def save(self):
        pass
    
