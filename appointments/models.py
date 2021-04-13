from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

import datetime as dt
#from administrators.models import Appointment, Invoice, Bill, Review

# Doctors models here.

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

	def total_revenue(self):
		invoices = Invoice.objects.filter(doctor=self.id)
		revenue = 0.0
		for inv in invoices:
			revenue = revenue + inv.total_amount 
		return revenue
	
	def review(self):
		reviews = Review.objects.filter(appointment__doctor=self.id)
		avg_review = 0
		if reviews.count() > 0:
			sum_review = 0
			for review in reviews:
				sum_review = sum_review + review.rate
			avg_review = sum_review//reviews.count()
		count = {}
		rate_val = avg_review + 1
		for x in range(1,rate_val):
			count.setdefault(x, 'filled')
		for x in range(rate_val,6):
			count.setdefault(x, ' ')
		return count

	def total_reviews(self):
		reviews = Review.objects.filter(appointment__doctor=self.id)
		return reviews.count()

	def availability(self):
		today = dt.date.today()
		duration = dt.timedelta(days=2)
		date = today + duration
		slot = 'unavailable'
		for x in range(1,8):
			day = str(f"{date:%A}").lower()
			schedule = DoctorSchedule.objects.get(doctor=self.id, day=day) # doctor, day, interval
			time_slots = TimeSlot.objects.filter(schedule=schedule.id) # schedule, start_time, end_time
			if time_slots.count() == 0:
				duration = dt.timedelta(days=1)
				date = date + duration
			else:
				appointments = Appointment.objects.filter(doctor=self.id, booking_date__date__gte=date)
				if appointments.count()==0:
					slot = "Available on "+str(f"{date:%a, %d %b}")
					break
				else:
					unavailable_time = []
					for appointment in appointments:
						unavailable_time += [appointment.booking_date.time]
					for slot in time_slots:
						if slot.start_time not in unavailable_time:
							slot = "Available on "+str(f"{date:%a, %d %b}")
							break
					if slot != 'unavailable':
						break
					else:
						duration = dt.timedelta(days=1)
						date = date + duration

		return slot

	def today_time_slots(self):
		now = timezone.now()
		day = str(f"{now:%A}").lower()
		schedule = DoctorSchedule.objects.get(doctor=self.id, day=day)
		time_slots = TimeSlot.objects.filter(schedule=schedule.id)
		return time_slots

	def open_now(self):
		now = timezone.now()
		day = str(f"{now:%A}").lower()
		schedule = DoctorSchedule.objects.get(doctor=self.id, day=day)
		time_slots = TimeSlot.objects.filter(schedule=schedule.id)
		for slot in time_slots:
			if now.time() > slot.start_time and now.time() < slot.end_time:
				return True
		return False

	def latest_degree(self):
		education = Education.objects.filter(doctor=self.id).order_by('y_o_c').reverse()[0]
		return education.degree

	def service_list(self):
		services = self.services
		return services.split(',')

	def specialization_list(self):
		specialization = self.specialization
		return specialization.split(',')

	def thumbs(self):
		reviews = Review.objects.filter(appointment__doctor=self.id)
		if reviews.count()>0:
			recommends = reviews.filter(recommend=True)
			if recommends.count()>0:
				percentage = recommends.count() / reviews.count() * 100
				return percentage
			else:
				return 0
		else:
			return 100

	def my_patient_id(self):
		appointments = Appointment.objects.filter(doctor=self.id)
		patients = []
		for appointment in appointments:
			if appointment.patient.id not in patients:
				patients += [appointment.patient.id]
		return patients


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


class SocialMedia(models.Model):
	doctor = models.OneToOneField(Doctor, on_delete=models.CASCADE)
	facebook_url = models.URLField('Facebook URL', max_length=200, blank=True)
	twitter_url = models.URLField('Twitter URL', max_length=200, blank=True)
	instagram_url = models.URLField('Instagram URL', max_length=200, blank=True)
	pinterest_url = models.URLField('Pinterest URL', max_length=200, blank=True)
	linkedin_url = models.URLField('Linkedin URL', max_length=200, blank=True)
	youtube_url = models.URLField('Youtube URL', max_length=200, blank=True)



# # # # Patients models here.

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

	def last_appointment(self):
		appointments = Appointment.objects.filter(patient=self.id).order_by('booking_date')
		if appointments.count()>0:
			index = appointments.count() - 1
			return appointments[index]
		else:
			return None


class Prescription(models.Model):
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
	doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
	date = models.DateTimeField('Prescription Date', auto_now_add=True)
	name = models.CharField('Name', max_length=50)
	quantity = models.FloatField('Quantity', default=0.0)
	days = models.FloatField('Prescription Days', default=0.00)
	morning = models.BooleanField('Morning', default=False)
	afternoon = models.BooleanField('Afternoon', default=False)
	evening = models.BooleanField('Evening', default=False)
	night = models.BooleanField('Night', default=False)
	# patient, doctor, name, quantity, days, morning, afternoon, evening, night

	def valid(self):
		duration = dt.timedelta(days=self.days)
		end_date = self.date + duration
		now = timezone.now()
		if now<end_date:
			return True
		else:
			return False

	def end_date(self):
		duration = dt.timedelta(days=self.days)
		end_date = self.date + duration
		return end_date


class MedicalRecord(models.Model):
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
	doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
	date_recorded = models.DateField('Record Date')
	description = models.CharField('Description', max_length=500, blank=True)
	attachment = models.FileField('Attachment', upload_to='File/Patient/MedicalRecords/', blank=True)
	date_added = models.DateTimeField('Added Date', auto_now_add=True)
	# patient, doctor, date_recorded, description, attachment


class Favourite(models.Model):
	doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
	fav_date = models.DateTimeField('Date Added', auto_now_add=True)


class Appointment(models.Model):
	doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
	purpose = models.CharField('Purpose', max_length=50)
	category = models.CharField('Type', max_length=50)
	amount = models.FloatField('Amount', default=0.00)
	status = models.CharField('Status', max_length=50)
	date = models.DateTimeField('Appointment Date', auto_now_add=True)
	booking_date = models.DateTimeField('Booking Date')
	follow_up_date = models.DateTimeField('Follow Up', null=True)
	# doctor, patient, purpose, category, amount, status, booking_date, follow_up_date

	def __str__(self):
		return self.apt_purpose

	def new_patient(self):
		appointments = Appointment.objects.filter(doctor=self.doctor.id, patient=self.patient.id)
		if appointments.count()>1:
			return "Old Patient"
		else:
			return "New Patient"


class Invoice(models.Model):
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
	doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
	total_amount = models.FloatField('Total Amount', default=0.00)
	date_paid = models.DateTimeField('Paid On', auto_now_add=True)
	# patient, doctor, total_amount, date_paid

	def bills(self):
		bills = Bill.objects.filter(invoice=self.id)
		return bills

	
class Bill(models.Model):
	invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, blank=True)
	appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, blank=True)
	description = models.CharField('Name', max_length=50)
	quantity = models.FloatField('Prescription Days', default=1.0)
	vat = models.FloatField('V.A.T', default=0.0)
	amount = models.FloatField('Amount', default=0.00)
	paid = models.BooleanField('Paid', default=False)
	# invoice, appointment, description, quantity, vat, amount, paid 

class Review(models.Model):
	appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, blank=True)
	date = models.DateTimeField('Review Date', auto_now_add=True)
	rate = models.IntegerField('Rate')
	recommend = models.BooleanField('Recommend', default=False)
	text = models.CharField('Review Title', max_length=150, blank=True)
	# appointment, date, rate, recommend, text

	def review_rate(self):
		count = {}
		rate_val = self.rate + 1
		for x in range(1,rate_val):
			count.setdefault(x, 'filled')
		for x in range(rate_val,6):
			count.setdefault(x, ' ')
		return count

	def total_reviews(self):
		query = Review.objects.filter(doctor=self.appointment.doctor.id)
		return len(query)

	def replies(self):
		replies = Reply.objects.filter(review=self.id)
		return replies

	def patient_liked(self):
		likes = LikedReview.objects.filter(user=self.appointment.patient.user.id, review=self.id)
		if likes.count()>0:
			return liked[0].recommend
		else:
			return None

	def doctor_liked(self):
		liked = LikedReview.objects.filter(user=self.appointment.doctor.user.id, review=self.id)
		if liked.count()>0:
			return liked[0].recommend
		else:
			return None

	def total_likes(self):
		likes = LikedReview.objects.filter(review=self.id, recommend=True)
		return likes.count()

	def total_dislikes(self):
		dislikes = LikedReview.objects.filter(review=self.id, recommend=False)
		return dislikes.count()


class Reply(models.Model):
	review = models.ForeignKey(Review, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	date = models.DateTimeField('Review Date', auto_now_add=True)
	text = models.CharField('Review Title', max_length=150)
	#review, user, text

	def get_user(self):
		usr = self.user
		group = usr.groups.get()
		if group.name=='patients_group':
			patient = Patient.objects.get(user=usr.id)
			return patient
		elif group.name=='doctors_group':
			doctor = Doctor.objects.get(user=usr.id)
			return doctor
		else:
			return user

	def get_group(self):
		usr = self.user
		group = usr.groups.get()
		return group.name


class LikedReview(models.Model):
	review = models.ForeignKey(Review, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	recommend = models.BooleanField('Recommend', default=False)
	# review, user, recommend


class LikedReply(models.Model):
	reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	recommend = models.BooleanField('Recommend', default=False)
