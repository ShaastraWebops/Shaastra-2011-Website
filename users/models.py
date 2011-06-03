from django.db import models
from django.contrib.auth.models import User
from main_test.events.models import Event

GENDER_CHOICES = (
    ('M','Male'),
    ('F','Female'),
)

STATE_CHOICES = (
	("Andhra Pradesh" , "Andhra Pradesh"),
	("Arunachal Pradesh" , "Arunachal Pradesh"),
	("Assam" , "Assam"),
	("Bihar" , "Bihar"),
	("Chhattisgarh" , "Chhattisgarh"),
	("Goa" , "Goa"),
	("Gujarat" , "Gujarat"),
	("Haryana" , "Haryana"),
	("Himachal Pradesh" , "Himachal Pradesh"),
	("Jammu And Kashmir" , "Jammu And Kashmir"),
	("Jharkhand" , "Jharkhand"),
	("Karnataka" , "Karnataka"),
	("Kerala" , "Kerala"),
	("Madhya Pradesh" , "Madhya Pradesh"),
	("Maharashtra" , "Maharashtra"),
	("Manipur" , "Manipur"),
	("Meghalaya" , "Meghalaya"),
	("Mizoram" , "Mizoram"),
	("Nagaland" , "Nagaland"),
	("Orissa" , "Orissa"),
	("Punjab" , "Punjab"),
	("Rajasthan" , "Rajasthan"),
	("Sikkim" , "Sikkim"),
	("Tamil Nadu" , "Tamil Nadu"),
	("Tripura" , "Tripura"),
	("Uttar Pradesh" , "Uttar Pradesh"),
	("Uttarakhand" , "Uttarakhand"),
	("West Bengal" , "West Bengal"),
	("Andaman And Nicobar Islands" , "Andaman And Nicobar Islands"),
	("Chandigarh" , "Chandigarh"),
	("Dadra And Nagar Haveli" , "Dadra And Nagar Haveli"),
	("Daman And Diu" , "Daman And Diu"),
	("Lakshadweep" , "Lakshadweep"),
	("NCT/Delhi" , "NCT/Delhi"),
	("Puducherry" , "Puducherry"),
	("Outside India" , "Outside India"),
)

#Just copy pasted last year's code. Will work just fine I guess

class College(models.Model):
    name=models.CharField (max_length = 255,help_text  = 'The name of your college. Please refrain from using short forms.')
    city=models.CharField (max_length = 30,help_text  = 'The name of the city where your college is located. Please refrain from using short forms.' )
    state=models.CharField (max_length = 40,choices    = STATE_CHOICES,help_text  = 'The state where your college is located. Select from the drop down list' )

    def __unicode__(self):
        return "%s, %s, %s"%(self.name, self.city, self.state)

    class Admin:
        pass


#User profile common to all users
#Author: Swaroop Ramaswamy - inital model                
class UserProfile(models.Model):
    user 			= models.ForeignKey		(User, unique = True)
    gender 			= models.CharField		(max_length = 1, choices = GENDER_CHOICES, default = 'F')   #Defaults to 'girl' ;-)
    age 			= models.IntegerField 	(default = 18 , help_text = 'You need to be over 12 and under 80 years of age to participate')
    branch 			= models.CharField		(max_length = 50, default = 'Enter Branch Here', blank = True, null=True, help_text = 'Your branch of study')
    mobile_number 	= models.CharField		(max_length = 15, null=True , help_text='Please enter your current mobile number')
    college 		= models.ForeignKey		(College)
    college_roll 	= models.CharField		(max_length = 40, default = 'Enter College Id/Roll No.', null=True)
    shaastra_id 	= models.CharField		(max_length = 20, unique = True, null=True)
    activation_key 	= models.CharField		(max_length = 40, null=True)
    key_expires 	= models.DateTimeField	(null=True)
    want_hospi 		= models.BooleanField	(default = False)
    is_coord        = models.BooleanField	(default = False)
    coord_event     = models.ForeignKey     (Event)
	
	    
    def __unicode__(self):
        return self.user.username

    class Admin:
        pass

# The "coord" model is being removed because when get_profile is called on a User instance, it will return only a UserProfile instance
# It will be very hard to get a "coord" instance afterwards
# Suggest using is_coord() to find out if a user is a coord
'''
class coord(UserProfile):
    event_name=models.ForeignKey(Event)
    department=models.CharField(max_length=80)
    # not sure if this is required
    #tdp= models.ManyToManyField(Question,blank=True,null=True)
     # not sure if a tdp field is required.
     # Can we handle it with just the question model??
    #Think about what else we need for a coord . We might need department etc
    #Could set college to IIT Madras, not implementing it right now to avoid confusion
    def set_coord():
        want_hospi=False
        pass
    
    class Admin:
        pass    
'''

# The whole Team models idea has been scrapped. Only working with "teams" in the submission model
'''            
#Author: Swaroop Ramaswamy - inital model        
class Team(models.Model):
    name = models.CharField (max_length=255)
    password = models.CharField (max_length=255)
    #Do we really need a team password ? 
    leader = models.ForeignKey(User, related_name="team_leader")
    members = models.ManyToManyField (User, related_name="team members")
    def __unicode__(self):
        return self.name

    class Admin:
        pass
'''
