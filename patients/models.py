from django.db import models
from django.contrib.auth.models import User

from doctors.models import Doctor

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


class MedicalRecord(models.Model):
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
	doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
	date_recorded = models.DateField('Record Date')
	description = models.CharField('Description', max_length=500, blank=True)
	attachment = models.FileField('Attachment', upload_to='File/Patient/MedicalRecords/', blank=True)
	date_added = models.DateTimeField('Added Date', auto_now_add=True)


class Invoice(models.Model):
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
	doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
	total_amount = models.FloatField('Total Amount', default=0.00)
	date_paid = models.DateTimeField('Paid On', auto_now_add=True)
	# patient, doctor, total_amount, date_paid

	
class Bill(models.Model):
	invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, blank=True)
	appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, blank=True)
	description = models.CharField('Name', max_length=50)
	quantity = models.FloatField('Prescription Days', default=1.0)
	vat = models.FloatField('V.A.T', default=0.0)
	amount = models.FloatField('Amount', default=0.00)
	paid = models.BooleanField('Paid', default=False)
	# invoice, appointment, description, quantity, vat, amount, paid 


class Favourite(models.Model):
	doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
	fav_date = models.DateTimeField('Date Added', auto_now_add=True)


class Review(models.Model):
	doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
	date = models.DateTimeField('Review Date', auto_now_add=True)
	rate = models.IntegerField('Rate')
	title = models.CharField('Review Title', max_length=50, blank=True)
	text = models.CharField('Review Title', max_length=150, blank=True)
	# doctor, patient, review_date, rate, review_title, review_text

	def review_rate(self):
		count = {}
		rate_val = self.rate + 1
		for x in range(1,rate_val):
			count.setdefault(x, 'filled')
		for x in range(rate_val,6):
			count.setdefault(x, ' ')
		return count

	def total_reviews(self):
		query = Review.objects.filter(doctor=self.doctor)
		return len(query)

	def replies(self):
		replies = Reply.objects.filter(review=self.id)
		return replies

	def patient_liked(self):
		liked = LikedReview.objects.filter(user=self.patient.user.id)
		if liked.count()>0:
			return liked[0].recommend
		else:
			return None

	def doctor_liked(self):
		liked = LikedReview.objects.filter(user=self.doctor.user.id)
		if liked.count()>0:
			return liked[0].recommend
		else:
			return None


class Reply(models.Model):
	review = models.ForeignKey(Review, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	date = models.DateTimeField('Review Date', auto_now_add=True)
	text = models.CharField('Review Title', max_length=150)

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


class LikedReply(models.Model):
	reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	recommend = models.BooleanField('Recommend', default=False)
