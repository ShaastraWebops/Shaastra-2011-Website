from django.db import models
from main_test.users.models import *

class photos(models.Model):
    photolink      = models.URLField()
    photoid        = models.AutoField(primary_key=True)
    rating         = models.FloatField (max_digits=7,decimal_places=2)
    groupnum       = models.IntegerField(blank=False, null=False)
    photo          = models.ImageField(upload_to=('/galleryfinal/%s',photoid)
    user           = models.Foreignkey(generic_user)
    
    def __str__(self):
        return str(self.photoid)
#Since photoid is an autofield it ll automatically increment and each photo will have a unique photo id. It ll be saved to galleryfinal/[photoid].jpg . The photo can be accessed with the help of the photo id. 

