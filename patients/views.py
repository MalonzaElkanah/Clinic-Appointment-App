# Create your views here.
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Patient, Appointment, Prescription, MedicalRecord, Invoice, Bill
from .forms import PatientForm
from doctors.models import Doctor, Education, Experience, Award, Membership, Registration
from doctors.models import DoctorSchedule, TimeSlot

import datetime as dt

def register(request):
	if request.is_ajax():
		user = User.objects.create_user(request.POST['email'], request.POST['email'], 
			request.POST['password'])
		if user.is_active:
			user.first_name = request.POST['first_name']
			user.save()
			try:
				pt_group = Group.objects.get(name="patients_group")
				user.groups.add(pt_group)
			except Exception:
				pt_group = Group.objects.create(name='patients_group')
				perm_pt_add = Permission.objects.get(codename='add_patient')
				perm_pt_del = Permission.objects.get(codename='delete_patient')
				perm_pt_chg = Permission.objects.get(codename='change_patient')
				pt_group.permissions.add(perm_pt_add, perm_pt_chg, perm_pt_del)
				user.groups.add(pt_group)
			return JsonResponse({"success": "User " + request.POST['first_name'] +" Created.", 
				"redirect": "../../login/"}, status=200)
		else:
			return JsonResponse({"error": "Error Creating User " + request.POST['first_name'] +"."}, 
				status=200) 
	else:
		return render(request, 'patients/register.html')


def check_patient(user):
	group = user.groups.get()
	return group.name == 'patients_group'


def check_settings(user):
	profile = Patient.objects.filter(user=user.id)
	return profile.count()>=1


@login_required(login_url='/login/')
@user_passes_test(check_patient, login_url='/login/')
@user_passes_test(check_settings, login_url='/patients/profile-settings/')
def patient_dashboard(request):
	profile = Patient.objects.get(user=request.user.id)
	appointments = Appointment.objects.filter(patient=profile.id)
	prescriptions = Prescription.objects.filter(patient=profile.id) 
	medical_records = MedicalRecord.objects.filter(patient=profile.id)
	invoices = Invoice.objects.filter(patient=profile.id)
	return render(request, 'patients/patient-dashboard.html', {"profile": profile, "appointments": appointments, 
		'prescriptions': prescriptions, 'medical_records': medical_records, 'invoices': invoices})


@login_required(login_url='/login/')
@user_passes_test(check_patient, login_url='/login/')
def profile_settings(request):
	#data = {'user': request.user.id, 'first_name': request.user.first_name, 'email': request.user.email}
	if request.method == 'POST':
		if int(request.POST['user']) == request.user.id:
			try:
				a = Patient.objects.get(user=request.user.id)
				f = PatientForm(request.POST, request.FILES, instance=a)
				f.save()
				return HttpResponseRedirect('../../patients/')
			except Exception:
				form = PatientForm(request.POST, request.FILES)
				if form.is_valid():
					form.save()
					user=request.user
					user.last_name = request.POST['second_name']
					user.first_name = request.POST['first_name']
					user.email = request.POST['email']
					user.save()
					return HttpResponseRedirect('../../patients/')
				else:
					return HttpResponse(form.errors)
					# return render(request, 'appointments/profile-settings.html', {'form': form})
		else:
			return HttpResponse("form.errors")
	else:
		profile = None
		try:
			profile = Patient.objects.get(user=request.user.id)
		except Exception:
			profile = request.user
		return render(request, 'patients/profile-settings.html', {"profile": profile})


def doctor_profile(request, slug, doctor_id):
	doctor = Doctor.objects.get(id=doctor_id)
	edu = Education.objects.filter(doctor=doctor_id) 
	exp = Experience.objects.filter(doctor=doctor_id)
	awd = Award.objects.filter(doctor=doctor_id)
	mbr = Membership.objects.filter(doctor=doctor_id)
	reg = Registration.objects.filter(doctor=doctor_id)
	return render(request, 'patients/doctor-profile.html', {"doctor": doctor, "education": edu, 
		"experience": exp, "award": awd, "membership": mbr, "registration": reg})


def booking(request, slug, doctor_id):
	#patient = Patient.objects.get(user=request.user.id)
	doctor = Doctor.objects.get(id=doctor_id)
	schedule = DoctorSchedule.objects.filter(doctor=doctor_id)
	today = dt.date.today()
	date = today + dt.timedelta(days=2)
	booking_dates = {}
	for x in range(1,8):
		day = str(f"{date:%A}")
		w_day = day.lower()
		schedule = DoctorSchedule.objects.get(doctor=doctor_id, day=w_day) # doctor, day, interval
		time_slots = TimeSlot.objects.filter(schedule=schedule.id) # schedule, start_time, end_time
		booking_time = []
		for time in time_slots:
			start_hour = int(f"{time.start_time:%H}")
			start_minute = int(f"{time.start_time:%M}")
			end_hour = int(f"{time.end_time:%H}")
			end_minute = int(f"{time.end_time:%M}")
			slot_interval = int(schedule.interval)
			while end_hour >= start_hour:
				book_time = dt.time(start_hour, start_minute)
				booking_time = booking_time +  [book_time] #[f"{book_time:%I.%M %p}"]
				start_minute = start_minute + slot_interval
				if start_minute>=60:
					start_hour = start_hour + 1
					start_minute = start_minute - 60

		if booking_time == []:
			booking_time = None
		booking_dates.setdefault(date, booking_time)
		date = date + dt.timedelta(days=1)

	return render(request, 'patients/booking.html', {"doctor": doctor, "schedule": schedule, 
		"booking_dates": booking_dates})


def checkout(request):
	if request.method == 'POST':
		doctor_id = int(request.POST['doctor'])
		doctor = Doctor.objects.get(id = doctor_id)
		# 12:00:00_17/03/2021
		time_date = str(request.POST['time_date']).split('_')
		time = time_date[0].split(':')
		date = time_date[1].split('/')
		book_date = dt.datetime(int(date[2]), int(date[1]), int(date[0]), int(time[0]), int(time[1], 0))
		profile = ""
		try:
			profile = Patient.objects.get(user = request.user.id)
		except Exception:
			profile = {}

		booking_fee = 100.0
		video_call = 50.0
		consultation_fee = doctor.pricing
		total_fee = booking_fee + video_call + consultation_fee

		return render(request, 'patients/checkout.html', {'book_date': book_date, 'doctor': doctor, 
			'profile': profile, 'booking_fee': booking_fee, 'video_call': video_call, 'total_fee': total_fee})
	else:
		pass

def booking_success(request):
	if request.method == 'POST':
		doctor_id = int(request.POST['doctor'])
		doctor = Doctor.objects.get(id = doctor_id)
		profile = ""
		try:
			profile = Patient.objects.get(user = request.user.id)
		except Exception:
			profile = {}

		booking_fee = 100.0
		video_call = 50.0
		consultation_fee = doctor.pricing
		total_fee = booking_fee + video_call + consultation_fee
		# Save the new Appointment to DB
		appointment = Appointment(doctor=doctor, patient=profile, purpose='General', category='General', 
			amount=total_fee, status='WAIT', booking_date=request.POST['date'])
		appointment.save()
		#Create Invoice
		invoice = Invoice(patient=profile, doctor=doctor, total_amount=total_fee)
		invoice.save()
		# Create Bills
		booking = Bill(invoice=invoice, appointment=appointment, description="Booking Fee", quantity=1.0, 
			vat=0.0, amount=booking_fee, paid=True)
		booking.save()
		video = Bill(invoice=invoice, appointment=appointment, description="Video Call Fee", quantity=1.0, 
			vat=0.0, amount=video_call, paid=True)
		video.save()
		consultation = Bill(invoice=invoice, appointment=appointment, description="Consultation Fee", 
			quantity=1.0, vat=0.0, amount=consultation_fee, paid=True)
		consultation.save()
		return render(request, 'patients/booking-success.html', {'appointment': appointment, 'invoice': invoice, 
			'profile': profile})
	else:
		pass


def invoice_view(request, slug, invoice_id):
	inv_id = int(invoice_id)
	invoice = Invoice.objects.get(id=inv_id)
	bills = Bill.objects.filter(invoice=invoice.id)
	profile = Patient.objects.get(user = request.user.id)
	return render(request, 'patients/invoice-view.html', {'invoice': invoice, 'bills': bills, 
		'profile': profile})


def change_password(request):
	return render(request, 'patients/change-password.html')


def chat(request):
	return render(request, 'patients/chat.html')

def favourites(request):
	return render(request, 'patients/favourites.html')
