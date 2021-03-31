from django import forms
from django.forms import ModelForm

from .models import Admin, AppSetting
from doctors.models import Speciality


class AdminForm(ModelForm):
	class Meta:
		model = Admin
		fields = ('user', 'image', 'first_name', 'second_name', 'd_o_b', 'phone_no', 'email', 'address_line', 
			'country', 'county', 'town')


class SpecialityForm(ModelForm):
	class Meta:
		model = Speciality
		fields = ('name', 'image')


class AppSettingForm(ModelForm):
	class Meta:
		model = AppSetting
		fields = ('logo', 'name', 'icon')
