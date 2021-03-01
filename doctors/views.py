from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.decorators import login_required, user_passes_test

from .forms import DoctorForm, EducationForm, ExperienceForm, AwardForm, MembershipForm, RegistrationForm
from .models import Doctor, Speciality, Education, Experience, Award, Membership, Registration

# Create your views here.

def doctor_register(request):
	if request.is_ajax():
		user = User.objects.create_user(request.POST['email'], request.POST['email'], 
			request.POST['password'])
		if user.is_active:
			user.first_name = request.POST['first_name']
			user.save()
			try:
				doc_group = Group.objects.get(name="doctors_group")
				user.groups.add(doc_group)
			except Exception:
				doc_group = Group.objects.create(name='doctors_group')
				perm_doc_add = Permission.objects.get(codename='add_doctor')
				perm_doc_del = Permission.objects.get(codename='delete_doctor')
				perm_doc_chg = Permission.objects.get(codename='change_doctor')
				doc_group.permissions.add(perm_doc_add, perm_doc_chg, perm_doc_del)
				user.groups.add(doc_group)
			return JsonResponse({"success": "User " + request.POST['first_name'] +" Created.", 
					"redirect": "../../login/"}, status=200)
		else:
			return JsonResponse({"error": "Error Creating User " + request.POST['first_name'] +"."}, 
				status=200) 
	else:
		return render(request, 'doctors/doctor-register.html')


def check_doctor(user):
	group = user.groups.get()
	return group.name=='doctors_group'


def check_settings(user):
	profile = Doctor.objects.filter(user=user.id)
	return profile.count()>=1


@login_required(login_url='/login/')
@user_passes_test(check_doctor, login_url='/login/')
@user_passes_test(check_settings, login_url='/doctors/profile-settings/')
def doctor_dashboard(request):
	profile = Doctor.objects.get(user=request.user.id)
	return render(request, 'doctors/doctor-dashboard.html', {"profile": profile})


@login_required(login_url='/login/')
@user_passes_test(check_doctor, login_url='/login/')
def doctor_profile_settings(request):
	if request.method == 'POST':
		if int(request.POST['user']) == request.user.id:
			try:
				a = Doctor.objects.get(user=request.user.id)
				f = DoctorForm(request.POST, request.FILES, instance=a)
				f.save()
				user=request.user
				user.last_name = request.POST['second_name']
				user.first_name = request.POST['first_name']
				user.email = request.POST['email']
				user.save()
				return HttpResponseRedirect('../profile/settings-page2/')
			except Exception:
				form = DoctorForm(request.POST, request.FILES)
				if form.is_valid():
					form.save()
					user=request.user
					user.last_name = request.POST['second_name']
					user.first_name = request.POST['first_name']
					user.email = request.POST['email']
					user.save()
					return HttpResponseRedirect('../profile/settings-page2/')
				else:
					return HttpResponse(form.errors)
					# return render(request, 'appointments/profile-settings.html', {'form': form})
		else:
			return HttpResponse("form.errors")
	else:
		profile = None
		try:
			profile = Doctor.objects.get(user=request.user.id)
		except Exception:
			pass
		specialities = Speciality.objects.all()
		return render(request, 'doctors/doctor-profile-settings.html', {'specialities': specialities, 
			'profile': profile})


@login_required(login_url='/login/')
@user_passes_test(check_doctor, login_url='/login/')
@user_passes_test(check_settings, login_url='/doctors/profile-settings/')
def doctor_profile_page2(request):
	profile = Doctor.objects.get(user=request.user.id)
	edu = Education.objects.filter(doctor=profile.id)
	exp = Experience.objects.filter(doctor=profile.id)
	awd = Award.objects.filter(doctor=profile.id)
	mbr = Membership.objects.filter(doctor=profile.id)
	reg = Registration.objects.filter(doctor=profile.id)
	if request.method == 'POST':
		#Education
		for a in edu:
			data = {"doctor": profile.id, "degree": request.POST['degree'+str(a.id)], 
			"institute": request.POST['institute'+str(a.id)], "y_o_c": request.POST['y_o_c'+str(a.id)]}
			form = EducationForm(data, instance=a)
			if form.is_valid():
				form.save()

		form_num = int(request.POST['edu_form-num'])
		for x in range(0,form_num):
			x = str(x)
			try:
				data = {"doctor": profile.id, "degree": request.POST['degree-'+x], 
				"institute": request.POST['institute-'+x], "y_o_c": request.POST['y_o_c-'+x]}
				form = EducationForm(data)
				if form.is_valid():
					form.save()
			except Exception:
				pass

		#, Experience
		for a in exp:
			data = {"doctor": profile.id, "hospital_name":  request.POST['hospital_name'+str(a.id)], 
			"start": request.POST['start'+str(a.id)], "finish": request.POST['finish'+str(a.id)], 
			"designation": request.POST['designation'+str(a.id)]}
			form = ExperienceForm(data, instance=a)
			if form.is_valid():
				form.save()

		form_num = int(request.POST['exp_form-num'])
		for x in range(0,form_num):
			x = str(x)
			try:
				data = {"doctor": profile.id, "hospital_name":  request.POST['hospital_name-'+x], 
				"start": request.POST['start-'+x], "finish": request.POST['finish-'+x], 
				"designation": request.POST['designation-'+x]}
				form = ExperienceForm(data)
				if form.is_valid():
					form.save()
			except Exception:
				pass

		#, Award, 
		for a in awd:
			data = {"doctor": profile.id, "award": request.POST['award'+str(a.id)], 
			"year": request.POST['year'+str(a.id)]}
			form = AwardForm(data, instance=a)
			if form.is_valid():
				form.save()

		form_num = int(request.POST['awd_form-num'])
		for a in range(0,form_num):
			a = str(a)
			try:
				data = {"doctor": profile.id, "award": request.POST['award-'+a], 
				"year": request.POST['year-'+a]}
				form = AwardForm(data)
				if form.is_valid():
					form.save()
			except Exception:
				pass

		# Membership, 
		for a in mbr:
			data = {"doctor": profile.id, "membership": request.POST['membership'+str(a.id)]}
			form = MembershipForm(data, instance=a)
			if form.is_valid():
				form.save()

		form_num = int(request.POST['mbr_form-num'])
		for a in range(0,form_num):
			a = str(a)
			try:
				data = {"doctor": profile.id, "membership": request.POST['membership-'+a]}
				form = MembershipForm(data)
				if form.is_valid():
					form.save()
			except Exception:
				pass

		#Registration
		for a in reg:
			data = {"doctor": profile.id, "year": request.POST['year'+str(a.id)], 
			"registration": request.POST['registration'+str(a.id)]}
			form = RegistrationForm(data, instance=a)
			if form.is_valid():
				form.save()

		form_num = int(request.POST['reg_form-num'])
		for a in range(0,form_num):
			a = str(a)
			try:
				data = {"doctor": profile.id, "year": request.POST['year-'+a], 
				"registration": request.POST['registration-'+a]}
				form = RegistrationForm(data)
				if form.is_valid():
					form.save()
			except Exception:
				pass

		return HttpResponseRedirect('../../../doctors/')
	else:
		return render(request, 'doctors/doctor-profile-page2.html', {'profile': profile, 'education': edu, 
			'experience': exp, 'awards': awd, 'membership': mbr, 'registration': reg})


def my_patients(request):
	return render(request, 'doctors/my-patients.html')

def add_billing(request):
	return render(request, 'doctors/add-billing.html')

def reviews(request):
	return render(request, 'doctors/reviews.html')

def doctor_profile(request):
	return render(request, 'doctors/doctor-profile.html')

def edit_billing(request):
	return render(request, 'doctors/edit-billing.html')

def add_prescription(request):
	return render(request, 'doctors/add-prescription.html')

def doctor_change_password(request):
	return render(request, 'doctors/doctor-change-password.html')

def chat_doctor(request):
	return render(request, 'doctors/chat-doctor.html')

def patient_profile(request):
	return render(request, 'doctors/patient-profile.html')

def invoices(request):
	return render(request, 'doctors/invoices.html')

def appointments(request):
	return render(request, 'doctors/appointments.html')

def edit_prescription(request):
	return render(request, 'doctors/edit-prescription.html')

def schedule_timings(request):
	return render(request, 'doctors/schedule_timings.html')

