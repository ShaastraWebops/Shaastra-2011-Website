from django.db import models

class photos(models.Model):
    photolink = models.Urlfield
    rating = models.FloatField (max_digits=7,decimal_places=2)
    groupnum = models.IntegerField(blank=False, null=False)
    photo= models.ImageField(upload_to='/galleryfinal')
    user=models.Foreignkey(generic_user)
    
    def __str__(self):
        return self.photolink


