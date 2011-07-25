# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm, SplitDateTimeWidget, RadioSelect
#from django.forms.fields import email_re

from django.contrib.auth.models import User
from django.template import Template, Context
import re
from main_test.confluence import models
from main_test.confluence.models import RSVP


class RSVPForm(ModelForm):
    class Meta:
        model=models.RSVP
    
    def clean_email(self):
        if RSVP.objects.filter(email=self.cleaned_data['email']):
            pass
        else:
            return self.cleaned_data['email']
        raise forms.ValidationError('This email address is already taken. Please choose another.')

