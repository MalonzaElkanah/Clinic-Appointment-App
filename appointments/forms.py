from django import forms
from django.forms import ModelForm

from .models import Doctor, Education, Experience, Award, Membership, Registration, SocialMedia
from .models import Patient, Prescription

# Doctors Forms

class DoctorForm(ModelForm):
	class Meta:
		model = Doctor
		fields = ('user', 'image', 'first_name', 'second_name', 'title', 'd_o_b', 'gender', 'biography', 
			'phone_no', 'email', 'address_line1', 'address_line2', 'country', 'county', 'town', 'pricing', 
			'services', 'specialization', 'clinic', 'clinic_address', 'speciality')

class EducationForm(ModelForm):
	class Meta:
		model = Education
		fields = ('doctor', 'degree', 'institute', 'y_o_c')

class ExperienceForm(ModelForm):
	class Meta:
		model = Experience
		fields = ('doctor', 'hospital_name', 'start', 'finish', 'designation')

class AwardForm(ModelForm):
	class Meta:
		model = Award
		fields = ('doctor', 'award', 'year')

class MembershipForm(ModelForm):
	class Meta:
		model = Membership
		fields = ('doctor', 'membership')

class RegistrationForm(ModelForm):
	class Meta:
		model = Registration
		fields = ('doctor', 'year', 'registration')


class SocialMediaForm(ModelForm):
	
	class Meta:
		model = SocialMedia
		fields = ('doctor', 'facebook_url', 'twitter_url', 'instagram_url', 'pinterest_url', 'linkedin_url', 
			'youtube_url')


class PrescriptionForm(ModelForm):

	class Meta:
		model = Prescription
		fields = ( 'patient', 'doctor', 'name', 'quantity', 'days', 'morning', 'afternoon', 'evening', 'night')


# Patients Forms

class PatientForm(ModelForm):
	class Meta:
		model = Patient
		fields = ('user', 'image', 'first_name', 'second_name', 'd_o_b', 'gender', 'blood_group', 'phone_no', 
			'email', 'street_lane', 'country', 'county', 'town')
