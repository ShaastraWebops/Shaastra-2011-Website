from django.db import models

# Create your models here.
class RSVP(models.Model):
    name    = models.CharField  ( max_length = 30, null = True )
    email   = models.EmailField ( null = True, unique=True )
    address =models.CharField  ( max_length = 30, null = True )
    mobile_number = models.CharField(max_length = 15, null=True )
    def __unicode__(self):
        return self.content
    
    class Admin:
        pass            
        
