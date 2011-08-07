from django.db import models
from django.contrib.auth.models import User

PROGRAMME_CHOICES = (
    ('1B', 'First (Bachelors Degree)'),
    ('2B', 'Second (Bachelors Degree)'),
    ('3B', 'Third (Bachelors Degree)'),
    ('4B', 'Fourth (Bachelors Degree)'),
    ('5B', 'Fifth (Bachelors Degree)'),
    ('1PG', 'First (Post Graduate Degree)'),
    ('2PG', 'Second (Post Graduate Degree)'),
    ('3PG', 'Third (Post Graduate Degree)'),
    ('4PG', 'Fourth (Post Graduate Degree)'),
)

def get_resume_path(instance, filename):
    return 'ambassador_submissions/' + filename

class ShaastraAmbassador(models.Model):
    user = models.ForeignKey(User, unique = True)
    college_url = models.URLField(null = True, blank = True)
    programme = models.CharField(max_length = 5, choices = PROGRAMME_CHOICES, blank = True)
    resume_file = models.FileField(upload_to = get_resume_path, blank = True)
    ques1 = models.TextField(
        blank = False, 
        verbose_name = 'Why would you like to be a "Shaastra Ambassador"?', 
        help_text = 'Write it in your own words - your motivation for the application.'
    )
    ques2 = models.TextField(
        blank = False, 
        verbose_name = 'List your ideas on "Inspiring the Future" Hint: Passing on the legacy to juniors (new participants) from seniors (experienced participants)',
        help_text = 'This will help us to link your thinking with the Shaastra 2011 theme : "Inspire the Future"'
    )
    ques3 = models.TextField(
        blank = True, 
        verbose_name = 'List the major achievements of your college -- awards, projects, prizes in other technical festivals etc',
        help_text = 'Please note that this will not necessarily have an impact on your selection. This is only to get an idea of achievements of your institute and the scale of technical enthusiasm'
    )
    ques4 = models.TextField(
        blank = True,
        verbose_name = 'Suggest ways of opening more channels of communication between the tech community in your college and that in other colleges -- such as IIT Madras',
        help_text = 'This will help us develop a stronger bond between the tech community of IIT Madras and that of your college and thus explore opportunities together.'
    )
    
    def __unicode__(self):
        return self.user.username

'''
Need to do:
    - Form validation - done
    - File upload - done (needs testing)
    - View for form filling and saving - done
    - Link on cores dashboard to see list of submissions
    - View for list of submissions - done
    - Configure the urls to point at the submission list and detail views
    - Write out the templates
'''

