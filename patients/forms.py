from django import forms
from django.forms import ModelForm

from .models import Patient


class PatientForm(ModelForm):
	class Meta:
		model = Patient
		fields = ('user', 'image', 'first_name', 'second_name', 'd_o_b', 'gender', 'blood_group', 'phone_no', 
			'email', 'street_lane', 'country', 'county', 'town')
