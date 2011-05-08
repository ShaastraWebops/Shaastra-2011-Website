from django.db import models
from django.contrib import admin
from django import forms

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=80)
    url = models.URLField(null=True,verify_exists=False, blank=True)
    start_time = models.DateTimeField(null=True,blank=True)
    end_time = models.DateTimeField(null=True,blank=True)
   
    
    def __str__(self):
        return self.name

    class Admin:
        pass
