from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class AppSetting(models.Model):
	logo = models.ImageField('Website Logo', upload_to='Image/Setting', max_length=500, blank=True)
	name = models.CharField('Website Name', max_length=50)
	icon =  models.ImageField('Favicon', upload_to='Image/Setting', max_length=500, blank=True)
	# logo, name, icon


class Admin(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField('Profile Image', upload_to='Image/Administrator', 
		max_length=500, default='dummy.png')
	first_name = models.CharField('First Name', max_length=50)
	second_name =  models.CharField('Second Name', max_length=50)
	d_o_b = models.DateField('Date of Birth')
	phone_no = models.CharField('Phone Number', max_length=50)
	email = models.EmailField('Email', max_length=250)
	address_line = models.CharField('Address Line', max_length=200, blank=True)
	country = models.CharField('Country', max_length=100, blank=True)
	county = models.CharField('County', max_length=100, blank=True)
	town = models.CharField('Town', max_length=100, blank=True)\
	# user, image, first_name, second_name, d_o_b, phone_no, email, address_line, country, county, town

	def __str__(self):
		return self.first_name+" "+self.second_name


