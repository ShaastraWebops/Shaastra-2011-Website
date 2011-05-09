# have written a very basic crude definition of events_all model




from django.db import models

class Tag(models.Model):
    name=models.CharField(max_length=30)
    def __str__(self):
        return self.name
    
    class Admin:
        pass


class Event_All(models.Model):
	name  =  models.CharField(max_length=30)
	url   =  models.URLField(verify_exists= True)
	tags  =  models.ManyToManyField(Tag)
	etype =  models.CharField(max_length=30)
	participants  =  models.ManyToManyField(User)
	start_time    =  models.DateTimeField(null= True, blank=True)
	end_time      =  models.DateTimeField(null= True , blank = True)
	coords        =  models.ManyToManyField(User)
	selected_users=  models.ManyToManyField(User)
	#flagged_by   =  models.ManyToManyField()
	is_registrable=  models.BooleanField()
	is_hospi_avail=  models.BooleanField(null=True)
	logo          =  models.ImageField(path="logos/", blank=True, null=True )
    sponslogo     =  models.ImageField(path=" sponslogos/" , blank = True, null =True)
	tabs          =  models.ManyToManyField(Tabs)

	def __str__(self):
		return self.name

	class Admin:
		pass

