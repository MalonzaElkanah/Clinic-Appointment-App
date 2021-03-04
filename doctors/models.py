from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Speciality(models.Model):
	name = models.CharField('Name', max_length=100)
	image = models.ImageField('Image', upload_to='Image/Speciality', max_length=500)	
	
	def __str__(self):
		return self.name


class Doctor(models.Model):
	"""docstring for Doctor"""
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField('Profile Image', upload_to='Image/Doctors', 
		max_length=500, default='dummy.png')
	first_name = models.CharField('First Name', max_length=50)
	second_name =  models.CharField('Second Name', max_length=50)
	title = models.CharField('Title', max_length=200, default='Dr.')
	phone_no = models.CharField('Phone Number', max_length=50)
	email = models.EmailField('Email', max_length=250)
	gender = models.CharField('Gender', max_length=10)
	d_o_b = models.DateField('Date of Birth', blank=True)
	biography = models.CharField('Biography', max_length=1000, blank=True)
	address_line1 = models.CharField('Address Line 1', max_length=200, blank=True)
	address_line2 = models.CharField('Address Line 2', max_length=200, blank=True)
	country = models.CharField('Country', max_length=100, blank=True)
	county = models.CharField('County', max_length=100, blank=True)
	town = models.CharField('Town', max_length=100, blank=True)
	pricing =  models.FloatField('Amount', default=0.00)
	services = models.CharField('Services', max_length=1000, blank=True)
	specialization = models.CharField('Specialization', max_length=1000, blank=True)
	clinic = models.CharField('Clinic', max_length=100, blank=True)
	clinic_address = models.CharField('Clinic Address', max_length=100, blank=True)
	speciality = models.OneToOneField(Speciality, on_delete=models.CASCADE)
	''' user, image, first_name, second_name, title, phone_no, email, gender, d_o_b, biography,
	address_line1, address_line2, country, county, town, pricing, services, specialization, clinic, 
	clinic_address, speciality'''
	def full_name(self):
		return self.title + " " + self.first_name + " " + self.second_name

	def service_list(self):
		services = self.services
		return services.split(',')

	def specialization_list(self):
		specialization = self.specialization
		return specialization.split(',')


class Education(models.Model):
	doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
	degree = models.CharField('Degree', max_length=50)
	institute = models.CharField('College/Institute', max_length=50)
	y_o_c = models.DateField('Year of Completion')
	# doctor, degree, institute, y_o_c


class Experience(models.Model):
	doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
	hospital_name = models.CharField('Hospital Name', max_length=50)
	start = models.DateField('From')
	finish = models.DateField('To', blank=True)
	designation = models.CharField('Designation', max_length=50)
	# doctor, hospital_name, start, finish, designation


class Award(models.Model):
	doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
	award = models.CharField('Award', max_length=50)
	year  = models.DateField('Year')
	# doctor, award, year


class Membership(models.Model):
	doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
	membership = models.CharField('Membership', max_length=50)
	# doctor, membership


class Registration(models.Model):
	doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
	year = models.DateField('Year')		
	registration = models.CharField('Registration', max_length=50)
	# doctor, year, registration


class DoctorSchedule(models.Model):
	doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
	day = models.CharField('Day', max_length=10)
	interval = models.IntegerField('Interval')
	# doctor, day, interval

	def all_timeslots(self):
		schedules = DoctorSchedule.objects.filter(doctor=self.doctor.id)
		slots = {}
		for schedule in schedules:
			day = 'slot_'+str(schedule.day)
			time_slots = TimeSlot.objects.filter(schedule=schedule.id)
			if time_slots == []:
				time_slots = None
			slots.setdefault(day, time_slots)
		return slots

	def timeslots(self):
		schedule = DoctorSchedule.objects.get(id=self.id)
		time_slots = TimeSlot.objects.filter(schedule=schedule.id)
		return time_slots


class TimeSlot(models.Model):
	schedule = models.ForeignKey(DoctorSchedule, on_delete=models.CASCADE)
	start_time = models.TimeField('Start Time') 
	end_time = models.TimeField('End Time')
	#schedule, start_time, end_time

	def slot(self):
		time = str(f"{self.start_time:%I.%M %p}")+" - "+str(f"{self.end_time:%I.%M %p}")
		return time

