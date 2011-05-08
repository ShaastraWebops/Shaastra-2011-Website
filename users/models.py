from django.db import models
from django.contrib import admin
from django import forms

GENDER_CHOICES = (
    ('M','Male'),
    ('F','Female'),
)
        

# Create your models here.
# Creating generic user so that coord and participant classes can be further derived from this. 
class generic_user(models.Model):

    user_name = models.CharField(unique=True, max_length=30) #Make it foreign key
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES,default='M')
    age = models.IntegerField(default=18,)
    branch = models.CharField(max_length=50,default='Enter Branch Here',blank=True)
    mobile_number = models.CharField(max_length=15)
    email_id = models.EmailField(max_length=150) #unique = True ?
    activation_key = models.CharField(max_length=40)
    key_expires = models.DateTimeField()
    
    def __str__(self):
        return self.user.username

    class Admin:
        pass
