from django.db import models
from django.conf import settings

from django import forms
from main_test.recaptcha import fields as recaptcha_fields
import os,os.path

class UploadFileForm(forms.Form):
    caption     = forms.CharField(max_length=500)
    file        = forms.ImageField()

class selectaphoto(forms.Form):
    selectedid     =forms.IntegerField()
    photoid1       =forms.IntegerField()
    photoid2       =forms.IntegerField()

class AddUserForm(forms.Form):

    first_name      = forms.CharField  (max_length=30,
                                       help_text='Enter your first name here.')
    last_name       = forms.CharField  (max_length=30,
                                       help_text='Enter your last name here.')
    username       = forms.CharField  (max_length=30,
                                       help_text='30 characters or fewer. Letters, numbers and @/./+/-/_ characters')
    email          = forms.EmailField (help_text='Enter your e-mail address. eg, someone@gmail.com')
    password       = forms.CharField  (min_length=6,
                                       max_length=30,
                                       widget=forms.PasswordInput,
                                       help_text='Enter a password that you can remember')
    password_again = forms.CharField  (max_length=30,
                                       widget=forms.PasswordInput,
                                       help_text='Enter the same password that you entered above')
    recaptcha      = recaptcha_fields.ReCaptchaField (label='Show us that you are not a bot!',
                                                      help_text='Enter the words shown in the space provided')                                       
                                       
    def clean_username(self):
        if not alnum_re.search(self.cleaned_data['username']):
           raise forms.ValidationError(u'Usernames can only contain letters, numbers and underscores')
        if User.objects.filter(username=self.cleaned_data['username']):
            pass
        else:
            return self.cleaned_data['username']
        raise forms.ValidationError('This username is already taken. Please choose another.')
        
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
                                                                   
class Photo(models.Model):
    # import os, os.path, Image
    photoid        = models.AutoField(primary_key=True)  
    image          = models.ImageField(upload_to=settings.MEDIA_ROOT)
    title          = models.CharField(max_length=80)
    kvalue         = models.IntegerField(blank=True, null=True) 
    rating         = models.IntegerField(blank=True, null=True)
    user           = models.CharField(max_length=80)
    caption        = models.CharField(max_length=500)
    
    def __str__(self):
        return str(self.photoid)
    class META:
        get_latest_by = 'date'

    class Admin:
        ordering = ['date']

    def __unicode__(self):
        return self.title
    def __str__(self):
        return self.__unicode__().encode('utf8', 'replace')
                
    def delete_thumbnails(self):
        """Remove thumbnail and display-sized images when deleting.

        This may fail if, for example, they don't exist, so it should
        fail silently.  It may not be a good idea to delete the
        original, as the user may not understand that deleting it from
        the gallery deletes it from the filesystem, so currently we
        don't do that.
        
        """
        try:
            os.unlink(self.thumbpath())
        except (IOError, OSError):
            pass
        try:
            os.unlink(self.disppath())
        except (IOError, OSError):
            pass
        # Deleting the original might be a bad thing.
        #os.unlink(self.fullpath())

