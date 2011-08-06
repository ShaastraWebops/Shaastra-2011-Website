from django.db import models
from django.contrib.auth.models import User

PROGRAMME_CHOICES = (
    'First (Bachelors Degree)',
    'Second (Bachelors Degree)',
    'Third (Bachelors Degree)',
    'Fourth (Bachelors Degree)',
    'Fifth (Bachelors Degree)',
    'First (Post Graduate Degree)',
    'Second (Post Graduate Degree)',
    'Third (Post Graduate Degree)',
    'Fourth (Post Graduate Degree)',
)

class ShaastraAmbassador(models.Model)
    user = models.ForeignKey(User, unique = True)
    college_url = models.URLField(null=True,blank=True)
    programme = models.ChoiceField(widget=RadioSelect, choices=PROGRAMME_CHOICES,blank=False)
    resume_file = models.FileField(blank=False)
    ques1 = models.TextField(blank=False,help_text = 'Write it in your own words - your motivation for the application.')
    ques2 = models.TextField(blank=False, help_text = 'This will help us to link your thinking with the Shaastra 2011 theme : "Inspire the Future"')
    ques3 = models.TextField(blank=False, help_text = 'Please note that this will not necessarily have an impact on your selection. This is only to get an idea of achievements of your institute and the scale of technical enthusiasm')
    ques4 = models.TextField(blank=False, help_text = 'This will help us develop a stronger bond between the tech community of IIT Madras and that of your college and thus explore opportunities together.')
    
