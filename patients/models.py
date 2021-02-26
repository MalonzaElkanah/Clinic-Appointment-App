from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Patient(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField('Profile Image', upload_to='Image/Patient/Profile/', 
		max_length=500, default='dummy.png')
	first_name = models.CharField('First Name', max_length=50)
	second_name = models.CharField('Second Name', max_length=50)
	d_o_b = models.DateField('Date Of Birth')
	gender = models.CharField('Gender', max_length=10)
	email = models.CharField('Email', max_length=50)
	phone_no = models.CharField('Phone Number', max_length=20)
	blood_group = models.CharField('Blood Group', max_length=5)
	country = models.CharField('Country', max_length=50)
	county = models.CharField('County', max_length=50)
	town = models.CharField('Town', max_length=50)
	street_lane = models.CharField('Street/Lane', max_length=50)
	
	def __str__(self):
		return self.first_name +' '+self.second_name 


