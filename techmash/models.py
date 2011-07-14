from django.db import models
from django.conf import settings

from django import forms
import os,os.path

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file  = forms.ImageField()

class selectaphoto(forms.Form):
    selectedid     =forms.IntegerField()
    photoid1       =forms.IntegerField()
    photoid2       =forms.IntegerField()

class Photo(models.Model):
    # import os, os.path, Image
    photoid        = models.AutoField(primary_key=True)  
    image          = models.ImageField(upload_to=settings.MEDIA_ROOT)
    title          = models.CharField(max_length=80)
    kvalue         = models.IntegerField(blank=True, null=True) 
    rating         = models.IntegerField(blank=True, null=True)
    user           = models.CharField(max_length=80)
    
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

