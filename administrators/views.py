from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone

from .models import AppSetting, Admin
from .forms import AdminForm, SpecialityForm, AppSettingForm
from appointments.models import Doctor,  Patient, Speciality, Appointment, Invoice, Review, Reply

import datetime as dt
# Create your views here.


def check_admin(user):
	return user.is_superuser


def check_settings(user):
	profile = Admin.objects.filter(user=user.id)
	return profile.count()>=1


@login_required(login_url='/login/')
@user_passes_test(check_admin, login_url='/login/')
def profile(request):
	profile = None
	form = None
	try:
		profile = Admin.objects.get(user=request.user.id)
		if request.method == 'POST':
			if int(request.POST['user']) == request.user.id:
				form = AdminForm(request.POST, request.FILES, instance=profile)
				if form.is_valid():
					form.save()
				else:
					return HttpResponse(formset.errors)
		form = AdminForm(instance=profile)

	except Exception:
		if request.method == 'POST':
			if int(request.POST['user']) == request.user.id:
				form = AdminForm(request.POST, request.FILES)
				if form.is_valid():
					form.save()
					user=request.user
					user.last_name = request.POST['second_name']
					user.first_name = request.POST['first_name']
					user.email = request.POST['email']
					user.save()
					return HttpResponseRedirect('../../administrators/profile/')
				else:
					return HttpResponse(formset.errors)
		else:
			form = AdminForm()
	return render(request, 'administrators/profile.html', {'profile': profile, 'form': form})


@login_required(login_url='/login/')
@user_passes_test(check_admin, login_url='/login/')
@user_passes_test(check_settings, login_url='/administrators/profile/')
def admin_dashboard(request):
	profile = Admin.objects.get(user=request.user.id)
	doctors = Doctor.objects.all()
	patients = Patient.objects.all()
	appointments = Appointment.objects.all()
	invoices = Invoice.objects.all()
	revenue = 0.0
	for inv in invoices:
		revenue = revenue + inv.total_amount 
	months_revenue = half_year_revenue()
	new_users = half_year_users()
	return render(request, 'administrators/index.html', {'profile': profile, 'doctors': doctors, 
		'patients': patients, 'appointments': appointments, 'invoices': invoices, 'total_revenue': revenue, 
		'months_revenue': months_revenue, 'new_users': new_users})


@login_required(login_url='/login/')
@user_passes_test(check_admin, login_url='/login/')
@user_passes_test(check_settings, login_url='/administrators/profile/')
def appointment_list(request):
	profile = Admin.objects.get(user=request.user.id)
	appointments = Appointment.objects.all()
	return render(request, 'administrators/appointment-list.html', {'profile': profile, 
		'appointments': appointments})


@login_required(login_url='/login/')
@user_passes_test(check_admin, login_url='/login/')
@user_passes_test(check_settings, login_url='/administrators/profile/')
def specialities(request):
	if request.method == 'POST':
		form = SpecialityForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
		return HttpResponseRedirect('../../administrators/specialities/')
	else:
		profile = Admin.objects.get(user=request.user.id)
		specialities = Speciality.objects.all()
		forms = {}
		for speciality in specialities:
			forms.setdefault(speciality, SpecialityForm(instance=speciality))
		return render(request, 'administrators/specialities.html', {'profile': profile, 'forms': forms,
			'specialities': specialities} )


@login_required(login_url='/login/')
@user_passes_test(check_admin, login_url='/login/')
@user_passes_test(check_settings, login_url='/administrators/profile/')
def delete_speciality(request):
	speciality = Speciality.objects.get(id=int(request.POST['speciality']))
	if request.method == 'POST':
		speciality.delete()
	return HttpResponseRedirect('../../administrators/specialities/')


@login_required(login_url='/login/')
@user_passes_test(check_admin, login_url='/login/')
@user_passes_test(check_settings, login_url='/administrators/profile/')
def edit_speciality(request):
	speciality = Speciality.objects.get(id=int(request.POST['speciality']))
	if request.method == 'POST':
		form = SpecialityForm(request.POST, request.FILES, instance=speciality)
		if form.is_valid():
			form.save()
		else:
			return HttpResponse(formset.errors)
	return HttpResponseRedirect('../../administrators/specialities/')


@login_required(login_url='/login/')
@user_passes_test(check_admin, login_url='/login/')
@user_passes_test(check_settings, login_url='/administrators/profile/')
def doctor_list(request):
	profile = Admin.objects.get(user=request.user.id)
	doctors = Doctor.objects.all()
	return render(request, 'administrators/doctor-list.html', {'profile': profile, 'doctors': doctors})


@login_required(login_url='/login/')
@user_passes_test(check_admin, login_url='/login/')
@user_passes_test(check_settings, login_url='/administrators/profile/')
def patient_list(request):
	profile = Admin.objects.get(user=request.user.id)
	patients = Patient.objects.all()
	return render(request, 'administrators/patient-list.html', {'profile': profile, 'patients': patients})


@login_required(login_url='/login/')
@user_passes_test(check_admin, login_url='/login/')
@user_passes_test(check_settings, login_url='/administrators/profile/')
def reviews(request):
	profile = Admin.objects.get(user=request.user.id)
	reviews = Review.objects.all()
	return render(request, 'administrators/reviews.html', {'profile': profile, 'reviews': reviews})


@login_required(login_url='/login/')
@user_passes_test(check_admin, login_url='/login/')
@user_passes_test(check_settings, login_url='/administrators/profile/')
def delete_review(request):
	if request.method == 'POST':
		review = Review.objects.get(id=int(request.POST['review']))
		speciality.delete()
	return HttpResponseRedirect('../../administrators/reviews/')


@login_required(login_url='/login/')
@user_passes_test(check_admin, login_url='/login/')
@user_passes_test(check_settings, login_url='/administrators/profile/')
def delete_reply(request):
	if request.method == 'POST':
		reply = Reply.objects.get(id=int(request.POST['reply']))
		reply.delete()
	return HttpResponseRedirect('../../administrators/reviews/')


@login_required(login_url='/login/')
@user_passes_test(check_admin, login_url='/login/')
@user_passes_test(check_settings, login_url='/administrators/profile/')
def transactions_list(request):
	profile = Admin.objects.get(user=request.user.id)
	invoices = Invoice.objects.all()
	return render(request, 'administrators/transactions-list.html', {'profile': profile, 'invoices': invoices})


@login_required(login_url='/login/')
@user_passes_test(check_admin, login_url='/login/')
@user_passes_test(check_settings, login_url='/administrators/profile/')
def settings(request):
	profile = Admin.objects.get(user=request.user.id)
	form = None
	app = None
	try:
		apps = AppSetting.objects.all()
		app = apps[0]
		if request.method == 'POST':
			if int(request.POST['user']) == request.user.id:
				form = AppSettingForm(request.POST, request.FILES, instance=app)
				if form.is_valid():
					form.save()
				else:
					return HttpResponse(form.errors)
		form = AppSettingForm(instance=app)

	except Exception:
		if request.method == 'POST':
			form = AppSettingForm(request.POST, request.FILES)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('../../administrators/settings/')
			else:
				return HttpResponse(form.errors)
		else:
			form = AppSettingForm()
	
	return render(request, 'administrators/settings.html', {'profile': profile, 'form': form, 'app': app})


@login_required(login_url='/login/')
@user_passes_test(check_admin, login_url='/login/')
@user_passes_test(check_settings, login_url='/administrators/profile/')
def invoice_report(request):
	profile = Admin.objects.get(user=request.user.id)
	invoices = Invoice.objects.all()
	return render(request, 'administrators/invoice-report.html', {'profile': profile, 'invoices': invoices})


@login_required(login_url='/login/')
@user_passes_test(check_admin, login_url='/login/')
@user_passes_test(check_settings, login_url='/administrators/profile/')
def change_password(request):
	profile = Admin.objects.get(user=request.user.id)
	if request.is_ajax():
		usr = request.user
		if usr.check_password(request.POST['old_password']):
			if request.POST['new_password'] == request.POST['confirm_password']:
				if not request.POST['new_password'] == request.POST['old_password']:
					usr.set_password(request.POST['new_password'])
					usr.save()
					logout(request)
					redirect = '../../login/'
					return JsonResponse({"success": "Password Updated.", "redirect": redirect}, status=200)
				else:
					return JsonResponse({"error": "The Password Has not Changed"}, status=200)
			else:
				return JsonResponse({"error": "Confirm and New Password don't Match"}, status=200)
		else:
			return JsonResponse({"error": "Incorrect password"}, status=200)
	else:
		return HttpResponseRedirect('../../administrators/profile/')


@login_required(login_url='/login/')
@user_passes_test(check_admin, login_url='/login/')
@user_passes_test(check_settings, login_url='/administrators/profile/')
def lock_screen(request):
	profile = Admin.objects.get(user=request.user.id)
	return render(request, 'administrators/lock-screen.html', {'profile': profile})


def forgot_password(request):
	return render(request, 'administrators/forgot-password.html')


def invoice(request):
	return render(request, 'administrators/invoice.html')


# Functions
def half_year_revenue():
	dic = {}
	months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
	today = timezone.now()
	six_months = dt.timedelta(days=183)
	date = today - six_months
	index1 = date.month - 1
	#Months in the Same Year
	if today.month > date.month:
		data_months = months[index1:today.month]
		for mnt in data_months:
			dic.setdefault(str(mnt), 0)
	else: 
		#Months in different Year
		data_months = months[index1:] + months[:today.month]
		for mnt in data_months:
			dic.setdefault(str(mnt), 0)

	invoices = Invoice.objects.filter(date_paid__gt=timezone.datetime(date.year, date.month, 1, 0, 0 ,0, 
		tzinfo=timezone.get_current_timezone())).order_by('date_paid')
	month_buffer = None
	total_amount = 0
	for inv in invoices:
		date = inv.date_paid
		dic.setdefault(str(f"{date:%b}"), total_amount)
		if month_buffer == None:
			month_buffer = str(f"{date:%b}")
			total_amount = total_amount + inv.total_amount
			dic[str(f"{date:%b}")] = total_amount
		elif month_buffer == str(f"{date:%b}"):
			total_amount = total_amount + inv.total_amount
			dic[str(f"{date:%b}")] = total_amount
		else:
			total_amount = inv.total_amount
			dic[str(f"{date:%b}")] = total_amount
			month_buffer = str(f"{date:%b}")

	return dic


def half_year_users():
	dic = {}
	dic1 = {}
	months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
	today = timezone.now()
	six_months = dt.timedelta(days=93)
	date = today - six_months
	index1 = date.month - 1
	#Months in the Same Year
	if today.month > date.month:
		data_months = months[index1:today.month]
		for mnt in data_months:
			dic.setdefault(str(mnt), 0)
			dic1.setdefault(str(mnt), 0)
	else: 
		#Months in different Year
		data_months = months[index1:] + months[:today.month]
		for mnt in data_months:
			dic.setdefault(str(mnt), 0)
			dic1.setdefault(str(mnt), 0)

	doctors = Doctor.objects.filter(user__date_joined__gt=timezone.datetime(date.year, date.month, 1, 0, 0 ,0, 
		tzinfo=timezone.get_current_timezone())).order_by('user')
	patients = Patient.objects.filter(user__date_joined__gt=timezone.datetime(date.year, date.month, 1, 0, 0 ,0, 
		tzinfo=timezone.get_current_timezone())).order_by('user')
	month_buffer = None
	total = 0
	for doc in doctors:
		date = doc.user.date_joined
		dic.setdefault(str(f"{date:%b}"), total)
		if month_buffer == None:
			month_buffer = str(f"{date:%b}")
			total = total + 1
			dic[str(f"{date:%b}")] = total
		elif month_buffer == str(f"{date:%b}"):
			total = total + 1
			dic[str(f"{date:%b}")] = total
		else:
			total_amount = 1
			dic[str(f"{date:%b}")] = total
			month_buffer = str(f"{date:%b}")

	total = 0
	for pat in patients:
		date = pat.user.date_joined
		dic1.setdefault(str(f"{date:%b}"), total)
		if month_buffer == None:
			month_buffer = str(f"{date:%b}")
			total = total + 1
			dic1[str(f"{date:%b}")] = total
		elif month_buffer == str(f"{date:%b}"):
			total = total + 1
			dic1[str(f"{date:%b}")] = total
		else:
			total = 1
			dic1[str(f"{date:%b}")] = total
			month_buffer = str(f"{date:%b}")

	data = {}
	for k, v in dic.items():
		data.setdefault(k , [v, dic1[k]]) 

	return data
