from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.decorators import login_required, user_passes_test

from .forms import DoctorForm, EducationForm, ExperienceForm, AwardForm, MembershipForm, RegistrationForm
from .forms import SocialMediaForm, PrescriptionForm
from .models import Doctor, Speciality, Education, Experience, Award, Membership, Registration, TimeSlot
from .models import DoctorSchedule, SocialMedia
from patients.models import Patient, Appointment, Invoice, Bill, Review, Prescription, MedicalRecord

import datetime as dt
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


@login_required(login_url='/login/')
@user_passes_test(check_doctor, login_url='/login/')
@user_passes_test(check_settings, login_url='/doctors/profile-settings/')
def doctor_dashboard(request):
	profile = Doctor.objects.get(user=request.user.id)
	appointments = Appointment.objects.filter(doctor=profile.id)
	upcoming_appointments = appointments.filter(booking_date__gte=dt.date.today())
	today_appointments = appointments.filter(status='ACCEPTTED', booking_date__date=dt.date.today())
	return render(request, 'doctors/doctor-dashboard.html', {"profile": profile, "appointments": appointments,
		"upcoming_appointments": upcoming_appointments, "today_appointments": today_appointments})


@login_required(login_url='/login/')
@user_passes_test(check_doctor, login_url='/login/')
@user_passes_test(check_settings, login_url='/doctors/profile-settings/')
def appointments(request):
	profile = Doctor.objects.get(user=request.user.id)
	appointments = Appointment.objects.filter(doctor=profile.id)
	return render(request, 'doctors/appointments.html', {'profile' :profile, 'appointments': appointments})


@login_required(login_url='/login/')
@user_passes_test(check_doctor, login_url='/login/')
@user_passes_test(check_settings, login_url='/doctors/profile-settings/')
def appointment_accept(request, slug, appointment_id):
	doctor = Doctor.objects.get(user=request.user.id)
	appointment = Appointment.objects.get(id=appointment_id)
	if appointment.doctor.id == doctor.id:
		appointment.status = 'ACCEPTTED'
		appointment.save()
		return JsonResponse({"success": "Appointment ACCEPTTED.", "redirect": "../../../../doctors/"}, 
			status=200)
	else:
		return JsonResponse({"error": "Error Updating Appointment"}, status=200) 


@login_required(login_url='/login/')
@user_passes_test(check_doctor, login_url='/login/')
@user_passes_test(check_settings, login_url='/doctors/profile-settings/')
def appointment_cancel(request, slug, appointment_id):
	doctor = Doctor.objects.get(user=request.user.id)
	appointment = Appointment.objects.get(id=appointment_id)
	if appointment.doctor.id == doctor.id:
		appointment.status = 'CANCELLED'
		appointment.save()
		return JsonResponse({"success": "Appointment CANCELLED.", "redirect": "../../../../doctors/"}, 
			status=200)
	else:
		return JsonResponse({"error": "Error Updating Appointment"}, status=200) 


@login_required(login_url='/login/')
@user_passes_test(check_doctor, login_url='/login/')
@user_passes_test(check_settings, login_url='/doctors/profile-settings/')
def appointment_complete(request, slug, appointment_id):
	doctor = Doctor.objects.get(user=request.user.id)
	appointment = Appointment.objects.get(id=appointment_id)
	if appointment.doctor.id == doctor.id:
		appointment.status = 'COMPLETED'
		appointment.save()
		return JsonResponse({"success": "Appointment COMPLETED.", "redirect": "../../../../doctors/"}, 
			status=200)
	else:
		return JsonResponse({"error": "Error Updating Appointment"}, status=200) 


@login_required(login_url='/login/')
@user_passes_test(check_doctor, login_url='/login/')
@user_passes_test(check_settings, login_url='/doctors/profile-settings/')
def my_patients(request):
	profile = Doctor.objects.get(user=request.user.id)
	appointments = Appointment.objects.filter(doctor=profile.id).exclude(status='CANCELLED')
	patients = []
	for appointment in appointments:
		if appointment.patient not in patients:
			patients += [appointment.patient]

	return render(request, 'doctors/my-patients.html', {'profile' :profile, 'patients': patients})


@login_required(login_url='/login/')
@user_passes_test(check_doctor, login_url='/login/')
@user_passes_test(check_settings, login_url='/doctors/profile-settings/')
def schedule_timings(request):
	profile = Doctor.objects.get(user=request.user.id)
	schedules = DoctorSchedule.objects.filter(doctor=profile.id)
	if schedules.count() < 7:
		res = new_schedule(profile)
		if res:
			schedules = DoctorSchedule.objects.filter(doctor=profile.id)
		else:
			return HttpResponse(res)

	hours = {}
	for i in range(0, 24):
		time = dt.time(i,00,00)
		time1 = dt.time(i,30,00)
		hours.setdefault(f"{time:%H:%M:%S}", f"{time:%I.%M %p}")
		hours.setdefault(f"{time1:%H:%M:%S}", f"{time1:%I.%M %p}")
	return render(request, 'doctors/schedule-timings.html', {'profile': profile, 'schedules': schedules, 
		"hours": hours})


@login_required(login_url='/login/')
@user_passes_test(check_doctor, login_url='/login/')
@user_passes_test(check_settings, login_url='/doctors/profile-settings/')
def new_timeslot(request):
	if request.method == 'POST':
		form_num = int(request.POST['add_form-num'])
		for x in range(0, form_num):
			if not request.POST['start_time_'+str(x)] == '' and not request.POST['end_time_'+str(x)] == '':
				schedule_id = int(request.POST['schedule']) 
				start =	request.POST['start_time_'+str(x)] 
				end = request.POST['end_time_'+str(x)]
				schedule = DoctorSchedule.objects.get(id=schedule_id)
				time_slot = TimeSlot(schedule=schedule, start_time=start, end_time=end)
				time_slot.save()

		redirect = '../schedule-timings/'	
		return JsonResponse({"success": "Time Slots Created.", "redirect": redirect}, status=200)
	else:
		return HttpResponseRedirect('../schedule-timings/')


@login_required(login_url='/login/')
@user_passes_test(check_doctor, login_url='/login/')
@user_passes_test(check_settings, login_url='/doctors/profile-settings/')
def update_timeslot(request):
	if request.method == 'POST':
		form_num = int(request.POST['edit_form-num'])
		schedule_id = int(request.POST['schedule'])
		schedule = DoctorSchedule.objects.get(id=schedule_id)
		time_slots = TimeSlot.objects.filter(schedule=schedule.id)
		for slot in time_slots:
			s = str(slot.id)
			if not request.POST['start_time'+s] == '' and not request.POST['end_time'+s] == '':
				slot.start_time = request.POST['start_time'+s]
				slot.end_time = request.POST['end_time'+s]
				slot.save()

		if form_num > 0:
			for x in range(0, form_num):
				if not request.POST['start_time_'+str(x)] == '' and not request.POST['end_time_'+str(x)] == '': 
					start =	request.POST['start_time_'+str(x)] 
					end = request.POST['end_time_'+str(x)]
					time_slot = TimeSlot(schedule=schedule, start_time=start, end_time=end)
					time_slot.save()

		redirect = '../schedule-timings/'	
		return JsonResponse({"success": "Time Slots Created.", "redirect": redirect}, status=200)
	else:
		return HttpResponseRedirect('../../schedule-timings/')


@login_required(login_url='/login/')
@user_passes_test(check_doctor, login_url='/login/')
@user_passes_test(check_settings, login_url='/doctors/profile-settings/')
def delete_timeslot(request, slug, slot_id):
	t_slots = TimeSlot.objects.get(id=slot_id)
	schdl = t_slots.schedule
	if schdl.doctor.user == request.user:
		t_slots.delete()
	return HttpResponseRedirect('../../../../schedule-timings/')


@login_required(login_url='/login/')
@user_passes_test(check_doctor, login_url='/login/')
@user_passes_test(check_settings, login_url='/doctors/profile-settings/')
def invoices(request):
	doctor = Doctor.objects.get(user=request.user.id)
	invoices = Invoice.objects.filter(doctor=doctor.id)
	return render(request, 'doctors/invoices.html', {'profile': doctor, 'invoices': invoices})


@login_required(login_url='/login/')
@user_passes_test(check_doctor, login_url='/login/')
@user_passes_test(check_settings, login_url='/doctors/profile-settings/')
def invoice(request, slug, invoice_id):
	doctor = Doctor.objects.get(user=request.user.id)
	inv_id = int(invoice_id)
	invoice = Invoice.objects.get(id=inv_id)
	bills = Bill.objects.filter(invoice=invoice.id)
	return render(request, 'patients/invoice-view.html', {'invoice': invoice, 'bills': bills, 
		'profile': doctor})


@login_required(login_url='/login/')
@user_passes_test(check_doctor, login_url='/login/')
@user_passes_test(check_settings, login_url='/doctors/profile-settings/')
def reviews(request):
	doctor = Doctor.objects.get(user=request.user.id)
	reviews = Review.objects.filter(doctor=doctor.id)
	return render(request, 'doctors/reviews.html', {'profile': doctor, 'reviews': reviews})


@login_required(login_url='/login/')
@user_passes_test(check_doctor, login_url='/login/')
@user_passes_test(check_settings, login_url='/doctors/profile-settings/')
def social_media(request):
	doctor = Doctor.objects.get(user=request.user.id)
	if request.method == 'POST':
		try:
			social = SocialMedia.objects.get(doctor=doctor.id)
			form = SocialMediaForm(request.POST, instance=social)
			if form.is_valid():
				form.save()
		except Exception:
			form = SocialMediaForm(request.POST)
			if form.is_valid():
				form.save()
		redirect = '../social-media/'	
		return JsonResponse({"success": "Social Sites Updated.", "redirect": redirect}, status=200)
	else:
		social = None
		try:
			social = SocialMedia.objects.get(doctor=doctor.id)
		except Exception:
			social = None
		return render(request, 'doctors/social-media.html', {'profile': doctor, 'social': social})


@login_required(login_url='/login/')
@user_passes_test(check_doctor, login_url='/login/')
@user_passes_test(check_settings, login_url='/doctors/profile-settings/')
def doctor_change_password(request):
	doctor = Doctor.objects.get(user=request.user.id)
	if request.is_ajax():
		usr = request.user
		if usr.check_password(request.POST['old_pswd']):
			if request.POST['new_pswd'] == request.POST['cfm_pswd']:
				if not request.POST['new_pswd'] == request.POST['old_pswd']:
					usr.set_password(request.POST['new_pswd'])
					usr.save()
					logout(request)
					redirect = '../../login/'
					return JsonResponse({"success": "Social Sites Updated.", "redirect": redirect}, status=200)
				else:
					return JsonResponse({"error": "The Password Has not Changed"}, status=200)
			else:
				return JsonResponse({"error": "Confirm and New Password don't Match"}, status=200)
		else:
			return JsonResponse({"error": "Incorrect password"}, status=200)
	else:
		return render(request, 'doctors/doctor-change-password.html', {'profile': doctor})


@login_required(login_url='/login/')
@user_passes_test(check_doctor, login_url='/login/')
@user_passes_test(check_settings, login_url='/doctors/profile-settings/')
def patient_profile(request, slug, patient_id):
	doctor = Doctor.objects.get(user=request.user.id)
	patient = Patient.objects.get(id=patient_id)
	appointments = Appointment.objects.filter(patient=patient_id, doctor=doctor.id)
	prescriptions = Prescription.objects.filter(patient=patient_id) 
	records = MedicalRecord.objects.filter(patient=patient_id) 
	invoices = Invoice.objects.filter(patient=patient_id, doctor=doctor.id)
	return render(request, 'doctors/patient-profile.html', {'profile': doctor, 'patient': patient, 
		'last_appointments': appointments, 'prescriptions': prescriptions, 'records': records, 
		'invoices': invoices})


@login_required(login_url='/login/')
@user_passes_test(check_doctor, login_url='/login/')
@user_passes_test(check_settings, login_url='/doctors/profile-settings/')
def add_prescription(request, slug, patient_id):
	doctor = Doctor.objects.get(user=request.user.id)
	patient = Patient.objects.get(id=patient_id)
	if request.method == 'POST':
		form_num = int(request.POST['form-num'])
		for x in range(0,form_num):
			x = str(x)
			#try:
			morning = None 
			afternoon = None 
			evening = None 
			night = None
			try:
				if request.POST['morning_'+x] == 'on':
					morning = True
			except Exception:
				morning = False

			try:
				if request.POST['afternoon_'+x] == 'on':
					afternoon = True
			except Exception:
				afternoon = False

			try:
				if request.POST['evening_'+x] == 'on':
					evening = True
			except Exception:
				evening = False

			try:
				if request.POST['night_'+x] == 'on':
					night = True
			except Exception:
				night = False
			#patient, doctor, name, quantity, days, 

			data = {"patient": patient_id, "doctor": doctor.id, "name": request.POST['name_'+x], 
			"quantity": request.POST['quantity_'+x], "days": request.POST['days_'+x], 
			"morning": morning, "afternoon": afternoon, "evening": evening, "night": night}
			form = PrescriptionForm(data)
			if form.is_valid():
				form.save()
			#except Exception:
			#	pass
		return HttpResponseRedirect('../../../patient_profile/'+slug+'/'+str(patient_id)+'/')
	else:
		return render(request, 'doctors/add-prescription.html', {'profile': doctor, 'patient': patient})


@login_required(login_url='/login/')
@user_passes_test(check_doctor, login_url='/login/')
@user_passes_test(check_settings, login_url='/doctors/profile-settings/')
def edit_prescription(request, patient_id, slug, prescription_id):
	doctor = Doctor.objects.get(user=request.user.id)
	patient = Patient.objects.get(id=patient_id)
	prescription = Prescription.objects.get(id=prescription_id)
	if patient_id == prescription.patient.id:
		if request.method == 'POST':
			form = PrescriptionForm(request.POST, instance=prescription)
			if form.is_valid():
				form.save()
			else:
				return HttpResponse(form.errors)
			prescription = Prescription.objects.get(id=prescription_id)
	return render(request, 'doctors/edit-prescription.html', {'profile': doctor, 'patient': patient,
		'prescription': prescription})


@login_required(login_url='/login/')
@user_passes_test(check_doctor, login_url='/login/')
@user_passes_test(check_settings, login_url='/doctors/profile-settings/')
def add_billing(request, slug, patient_id, appointment_id):
	doctor = Doctor.objects.get(user=request.user.id)
	patient = Patient.objects.get(id=patient_id)
	appointment = Appointment.objects.get(id=appointment_id, patient=patient_id, doctor=doctor.id)
	if request.method == 'POST':
		form_num = int(request.POST['form-num'])
		total_amount = 0
		for x in range(0,form_num):
			x = str(x)
			total_amount += float(request.POST['amount_'+x])
		#Create Invoice
		invoice = Invoice(patient=patient, doctor=doctor, total_amount=total_amount)
		invoice.save()
		# Create Bills
		for x in range(0,form_num):
			x = str(x)
			bill = Bill(invoice=invoice, appointment=appointment, description=request.POST['title_'+x], 
				quantity=1.0, vat=0.0, amount=float(request.POST['amount_'+x]), paid=True)
			bill.save()
		return HttpResponseRedirect('../../../../patient_profile/'+slug+'/'+str(patient_id)+'/')
	else:
		return render(request, 'doctors/add-billing.html', {'profile': doctor, 'patient': patient})

def doctor_profile(request):
	return render(request, 'doctors/doctor-profile.html')

def edit_billing(request):
	return render(request, 'doctors/edit-billing.html')

def chat_doctor(request):
	return render(request, 'doctors/chat-doctor.html')


def new_schedule(doctor):
	days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
	err = []
	for day in days:
		data = DoctorSchedule(doctor = doctor, day = day, interval = 30)
		data.save()
		
	return True
	