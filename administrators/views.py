from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import AppSetting, Admin

# Create your views here.


def check_admin(user):
	return user.is_superuser


def check_settings(user):
	profile = Admin.objects.filter(user=user.id)
	return profile.count()>=1


@login_required(login_url='/login/')
@user_passes_test(check_admin, login_url='/login/')
def profile(request):
	if request.method == 'POST':
		if int(request.POST['user']) == request.user.id:
			pass
	else:
		profile = None
		try:
			profile = Admin.objects.get(user=request.user.id)
		except Exception:
			pass
	return render(request, 'administrators/profile.html', {'profile': profile})


@login_required(login_url='/login/')
@user_passes_test(check_admin, login_url='/login/')
@user_passes_test(check_settings, login_url='/administrators/profile/')
def admin_dashboard(request):
	return render(request, 'administrators/index.html')


def transactions_list(request):
	return render(request, 'administrators/transactions-list.html')

def patient_list(request):
	return render(request, 'administrators/patient-list.html')

def lock_screen(request):
	return render(request, 'administrators/lock-screen.html')

def appointment_list(request):
	return render(request, 'administrators/appointment-list.html')

def reviews(request):
	return render(request, 'administrators/reviews.html')

def specialities(request):
	return render(request, 'administrators/specialities.html')

def forgot_password(request):
	return render(request, 'administrators/forgot-password.html')

def settings(request):
	return render(request, 'administrators/settings.html')

def doctor_list(request):
	return render(request, 'administrators/doctor-list.html')

def invoice_report(request):
	return render(request, 'administrators/invoice-report.html')

def invoice(request):
	return render(request, 'administrators/invoice.html')
