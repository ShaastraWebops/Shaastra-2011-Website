# -*- coding: utf-8 -*-
#We can use the same forms as last time for registation. We are not really changing anything here so.
#If we have to change anything it shouldn't be much of a problem
from django import forms
from django.db import models as d_models
import re 
from django.contrib.auth.models import User
from django.template import Template, Context
from django.utils.safestring import mark_safe

#from userportal.recaptcha import fields as recaptcha_fields

<<<<<<< HEAD
#from userportal.misc import util
from main_test.misc import util
#from userportal import settings
from main_test import settings

#from userportal.registration import models
#from userportal.events import models

=======
from main_test.misc import util
from main_test import settings

>>>>>>> 6a79896a607fc88a78d42162c8fceb7c97b00e79
from main_test.users import models
from main_test.events import models

alnum_re = re.compile(r'^[\w.-]+$') # regexp. from jamesodo in #django  [a-zA-Z0-9_.]
alphanumric = re.compile(r"[a-zA-Z0-9]+$")

GENDER_CHOICES = (
        (1, 'Male'),
        (2, 'Female'),
        )

HOSPI_CHOICES = (
        (1, 'Yes.'),
        (0, 'No.'),
        )

#COLLEGE_CHOICES = [(e.id, "%s, %s, %s"%(e.state,e.city,e.name)) for e in models.College.objects.order_by("state","city","name",)]

#Added to render the radio buttons horizontally
class HorizRadioRenderer(forms.RadioSelect.renderer):
    #this overrides widget method to put radio buttons horizontally instead of vertically.
    def render(self):
            #Outputs radios
            return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

class AddCollegeForm (forms.ModelForm):
    class Meta:
        model = models.College

class ConvertCoordForm(forms.Form):
    username=forms.CharField(max_length=30)
    event=forms.ModelChoiceField(queryset=models.Event.objects.all(), required = False)
    team_event=forms.ModelChoiceField(queryset=models.TeamEvent.objects.all(), required = False)

class AddCoordForm(forms.Form):
    username=forms.CharField(max_length=30)
    first_name=forms.CharField(max_length=30)
    last_name=forms.CharField(max_length=30)
    email=forms.EmailField()
    password=forms.CharField(max_length=30, widget=forms.PasswordInput)
    password_again=forms.CharField(max_length=30, widget=forms.PasswordInput)
    mobile_number=forms.CharField(max_length=15,required=False)
    event=forms.ModelChoiceField(queryset=models.Event.objects.all(), required = False)
    team_event=forms.ModelChoiceField(queryset=models.TeamEvent.objects.all(), required = False)

    def clean_password(self):
        if self.prefix:
            field_name1 = '%s-password'%self.prefix
            field_name2 = '%s-password_again'%self.prefix
        else:
            field_name1 = 'password'
            field_name2 = 'password_again'
            
        if self.data[field_name1] != '' and self.data[field_name1] != self.data[field_name2]:
            raise forms.ValidationError ("The entered passwords do not match.")
        else:
            return self.data[field_name1]

class JoinTeamForm(forms.Form):
    teamname=forms.CharField(max_length=30,help_text='The name of the team which you want to join. Your team leader can supply this information.')
    password=forms.CharField(max_length=30, widget=forms.PasswordInput, help_text='The password as given by your team leader.')

class MassRegisterForm (forms.Form):
    extra_users=forms.IntegerField(min_value=1)

class AddTeamForm(forms.Form):
    teamname=forms.CharField(max_length=30)
    password=forms.CharField(max_length=30, widget=forms.PasswordInput)
    password_again=forms.CharField(max_length=30, widget=forms.PasswordInput)
    
    def clean_teamname(self):
        if not alnum_re.search(self.cleaned_data['teamname']):
            raise forms.ValidationError(u'Team names can only contain letters, numbers and underscores')
        if models.Team.objects.filter(name=self.cleaned_data['teamname']):
            raise forms.ValidationError('This team name is already taken. Please choose another.')
        else:
            return self.cleaned_data['teamname']

    def clean_password(self):
        if self.prefix:
            field_name1 = '%s-password'%self.prefix
            field_name2 = '%s-password_again'%self.prefix
        else:
            field_name1 = 'password'
            field_name2 = 'password_again'
            
        if self.data[field_name1] != '' and self.data[field_name1] != self.data[field_name2]:
            raise forms.ValidationError ("The entered passwords do not match.")
        else:
            return self.data[field_name1]
    
class AddUserForm(forms.Form):
    username=forms.CharField(max_length=30,help_text='Enter a username. eg, siddharth_s')
    first_name=forms.CharField(max_length=30,help_text='Enter your first name. eg, Siddharth')
    last_name=forms.CharField(max_length=30,help_text='Enter your last name. eg, Swaminathan')
    gender=forms.ChoiceField(choices=GENDER_CHOICES,help_text='Select Male or Female')
    age=forms.IntegerField(min_value=1,help_text='Enter your age. eg, 18')
    branch=forms.CharField(max_length=50,help_text='Select your branch from the list. If it does not show up, please select the "Other" option.')
    email=forms.EmailField(help_text='Enter your e-mail address. eg, someone@gmail.com')
    password=forms.CharField(min_length=6, max_length=30, widget=forms.PasswordInput,help_text='Enter a password that you can remember')
    password_again=forms.CharField(max_length=30, widget=forms.PasswordInput,help_text='Enter the same password that you entered above')
    mobile_number=forms.CharField(max_length=15,help_text='Enter your mobile number. eg, 9884098840')
    college_roll=forms.CharField(label="College Id/Roll Number",max_length=40,help_text='Your college roll number. eg, ME09B053')
    college = forms.CharField(max_length=120,widget=forms.TextInput(attrs={'id':'coll_input'}),help_text='Select your college from the list. If it is not there, use the link below')
    #recaptcha = recaptcha_fields.ReCaptchaField(label='Show us that you are not a bot!',help_text='Enter the words shown in the space provided')
    want_hospi = forms.CharField(label='Want to be considered for accommodation ?',required=True,widget=forms.RadioSelect(renderer=HorizRadioRenderer,choices=HOSPI_CHOICES), help_text='In case you want accomodation. Please check the list of events for which accomodation will be provided before applying.')
    
    
    def clean_username(self):
        if not alnum_re.search(self.cleaned_data['username']):
           raise forms.ValidationError(u'Usernames can only contain letters, numbers and underscores')
        if User.objects.filter(username=self.cleaned_data['username']):
            pass
        else:
            return self.cleaned_data['username']
        raise forms.ValidationError('This username is already taken. Please choose another.')

    def clean_age(self):
	if (self.cleaned_data['age']>80 or self.cleaned_data['age']<12):
	    raise forms.ValidationError(u'Please enter an acceptable age (12 to 80)')
	else:
	    return self.cleaned_data['age']
	    
    def clean_mobile_number(self):
	if (len(self.cleaned_data['mobile_number'])!=10 or (self.cleaned_data['mobile_number'][0]!='7' and self.cleaned_data['mobile_number'][0]!='8' and self.cleaned_data['mobile_number'][0]!='9') or (not self.cleaned_data['mobile_number'].isdigit())):
	    raise forms.ValidationError(u'Enter a valid mobile number')
	else:
	  return self.cleaned_data['mobile_number']
	  
    def clean_first_name(self):
	if not self.cleaned_data['first_name'].replace(' ','').isalpha():
	    raise forms.ValidationError(u'Names cannot contain anything other than alphabets.')
	else:
	    return self.cleaned_data['first_name']
	  
    def clean_last_name(self):
	if not self.cleaned_data['last_name'].replace(' ','').isalpha():
	    raise forms.ValidationError(u'Names cannot contain anything other than alphabets.')
	else:
	    return self.cleaned_data['last_name']

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']):
            pass
        else:
            return self.cleaned_data['email']
        raise forms.ValidationError('This email address is already taken. Please choose another.')

    def clean_password(self):
        if self.prefix:
            field_name1 = '%s-password'%self.prefix
            field_name2 = '%s-password_again'%self.prefix
        else:
            field_name1 = 'password'
            field_name2 = 'password_again'
            
        if self.data[field_name1] != '' and self.data[field_name1] != self.data[field_name2]:
            raise forms.ValidationError ("The entered passwords do not match.")
        else:
            return self.data[field_name1]
	    
    def clean_college(self):
        coll_input = self.cleaned_data['college']
        try:
            coll_name, coll_city = coll_input.rsplit(',',1)
            collchk = models.College.objects.get(name = coll_name, city=coll_city)
        except: 
            raise forms.ValidationError ("Invalid college name, or college does not exist. Please use add college form below to add your college if it does not already exist")
        if(collchk):
            return collchk
        else :
            raise forms.ValidationError ("The College that you entered Does not exist or was Not Right")
    
    def clean_college_roll(self):
        if (not alphanumric.search(self.cleaned_data['college_roll'])) or self.cleaned_data['college_roll'].isalpha():
           raise forms.ValidationError(u'Enter a valid roll number.')
        else:
           return self.cleaned_data['college_roll']
    
class ModifyUserForm(forms.ModelForm):
    password1=forms.CharField(max_length=30,required=False,label="Password", widget=forms.PasswordInput)
    password2=forms.CharField(max_length=30, required=False,label="Verfiy Password", widget=forms.PasswordInput)
    class Meta:
        model = models.User 
        fields = ('email',)
    def clean_password1(self):
        if self.prefix:
            field_name1 = '%s-password1'%self.prefix
            field_name2 = '%s-password2'%self.prefix
        else:
            field_name1 = 'password'
            field_name2 = 'password_again'
            
        if self.data[field_name1] != '' and self.data[field_name1] != self.data[field_name2]:
            raise forms.ValidationError ("The entered passwords do not match.")
        else:
            return self.data[field_name1]

class ModifyUserProfileForm(forms.ModelForm):
    want_hospi=forms.BooleanField(label='Would you like to register for accomodation?', required=False)
    want_newsletter=forms.BooleanField(label="Would you like to receive Shaastra updates?", required=False)
    college_roll=forms.CharField(max_length=40,label="College Id / Roll Number")
        
    class Meta:
        model = models.UserProfile
#        fields = ('want_hospi','gender','age','branch','mobile_number','college_roll','want_newsletter',)
        fields = ('gender','age','branch','mobile_number','college_roll','want_newsletter','want_hospi')
#Uncomment the want_hospi and the fields and comment the second fields to get the hospi accomodation field in profile page.

class ModifyCompleteUserProfileForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        fields = ('first_name', 'last_name', 'gender', 'age', 'branch', 'mobile_number', 'college', 'college_roll','id_type')

class UserLoginForm(forms.Form):
    username=forms.CharField(help_text='Your username as registered with the Shaastra Userportal')
    password=forms.CharField(widget=forms.PasswordInput, help_text='Your password. If you do not remember this, please use the link below')

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()        
