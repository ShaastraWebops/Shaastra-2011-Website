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
    groupnum       = models.IntegerField(blank=True, null=True) 
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

    def thumbpath(self):
        """Path to the thumbnail
        """
        photobase = self.image[len(STOCKPHOTO_BASE)+1:]
        return os.path.join( settings.MEDIA_ROOT, STOCKPHOTO_BASE,
                     "cache", "thumbs", photobase)

    def thumburl(self):
        """URL to the thumbnail
        """
        photobase = self.image[len(STOCKPHOTO_BASE)+1:]
        # for windows -- to avoid urls with '\' in them
        if os.sep != '/':
            photobase = photobase.replace(os.sep, '/')
        if settings.MEDIA_URL.endswith('/'):
            return settings.MEDIA_URL + STOCKPHOTO_BASE + \
                "/cache/thumbs/" + photobase
        return settings.MEDIA_URL + '/' + STOCKPHOTO_BASE + \
            "/cache/thumbs/" + photobase
            

    def disppath(self):
        photobase = self.image[len(STOCKPHOTO_BASE)+1:]
        return os.path.join( settings.MEDIA_ROOT, STOCKPHOTO_BASE,
                         "cache", photobase)

    def dispurl(self):
        photobase = self.image[len(STOCKPHOTO_BASE)+1:]
        # for windows -- to avoid urls with '\' in them
        if os.sep != '/':
            photobase = photobase.replace(os.sep, '/')
        if settings.MEDIA_URL.endswith('/'):
            return settings.MEDIA_URL + STOCKPHOTO_BASE + "/cache/" \
                + photobase
        return settings.MEDIA_URL + '/' + STOCKPHOTO_BASE + \
            "/cache/" + photobase            

    def fullpath(self):
        if self.image.startswith('/'):
            return self.image
        return os.path.join(settings.MEDIA_ROOT, self.image)

    def fullurl(self):
        if self.image.startswith('/'):    
            # Shouldn't happen anymore
            return (settings.MEDIA_URL +
                    self.image[len(settings.MEDIA_ROOT):])
        else:
            if settings.MEDIA_URL.endswith('/'):
                return settings.MEDIA_URL + self.image
            return settings.MEDIA_URL + '/' + self.image
        

    def next(self):
        '''Return id of 'next' photo in the same gallery or None if at
        the end.'''
        # we could probably be more clever here by using the new nifty 
        # db access filters and queries, but for now, this is good enough
        photo_list = [x for x in self.gallery.photo_set.all()]
        ind = photo_list.index(self)
        if (ind +1) == len(photo_list):
            return None
        else:
            return photo_list[ind + 1]

    def prev(self):
        """Return id of 'previous' photo in the same gallery or None
        if at the beginning
        """
        photo_list = [x for x in self.gallery.photo_set.all()]
        ind = photo_list.index(self)
        if ind == 0:
            return False
        else:
            return photo_list[ind - 1]

    def full_exists(self):
        return os.path.exists( self.fullpath() )

    def disp_exists(self):
        return os.path.exists( self.disppath() )

    def thumb_exists(self):
        return os.path.exists( self.thumbpath() )

    def create_disp(self):
        im = Image.open( self.fullpath() )
        format = im.format
        # create the path for the display image
        disp_path = self.disppath()
        disp_dir = os.path.dirname(disp_path)
        if not os.path.exists(disp_dir):
            os.makedirs(disp_dir, 0775)

        # Make a copy of the image, scaled, if needed.
        im.thumbnail((self.gallery.display_width,
                      self.gallery.display_height),
                     Image.ANTIALIAS)
        im.save(disp_path, format)

    def create_thumb(self):
        im = Image.open( self.fullpath() )
        format = im.format
        # create the path for the thumbnail image
        thumb_path = self.thumbpath()
        thumb_dir = os.path.dirname(thumb_path)
        if not os.path.exists(thumb_dir):
            os.makedirs(thumb_dir, 0775)

        # Make a copy of the image, scaled, if needed.
        im.thumbnail((self.gallery.thumbnail_width,
                      self.gallery.thumbnail_height),
                     Image.ANTIALIAS)
        im.save(thumb_path, format)

    def build_display_images(self):
        """Make thumbnail and display-sized images after saving.
        
        For some reason, this may fail on a first pass (self.image may
        be empty when this is called), but if we just let it fail
        silently, it will apparently get called again and succeed.
        """
        if self.image:
            if not self.thumb_exists():
                self.create_thumb()
            if not self.disp_exists():
                self.create_disp()

# Create your models here.
