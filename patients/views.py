# Create your views here.
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.decorators import login_required

from .models import Patient


def register(request):
	if request.is_ajax():
		user = User.objects.create_user(request.POST['email'], request.POST['email'], request.POST['password'])
		if user.is_active:
			user.first_name = request.POST['first_name']
			user.save()
			try:
				pt_group = Group.objects.get(name="patients_group")
				user.groups.add(pt_group)
				return HttpResponseRedirect('../login')
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


def patient_dashboard(request):
	profile = check_profile(request.user)
	if profile == None:
		return HttpResponseRedirect('../patients/profile-settings/')
	else:
		return render(request, 'patients/patient-dashboard.html', {"profile": profile})


def profile_settings(request):
	return render(request, 'patients/profile-settings.html')


def booking(request):
	return render(request, 'patients/booking.html')


def booking_success(request):
	return render(request, 'patients/booking-success.html')


def checkout(request):
	return render(request, 'patients/checkout.html')


def change_password(request):
	return render(request, 'patients/change-password.html')


def doctor_profile(request):
	return render(request, 'patients/doctor-profile.html')

def chat(request):
	return render(request, 'patients/chat.html')

def invoice_view(request):
	return render(request, 'patients/invoice-view.html')


def favourites(request):
	return render(request, 'patients/favourites.html')


def check_profile(user):
	profile = None
	group = user.groups.get()
	if group.name=='patients_group':
		try:
			profile = Patient.objects.get(user=user.id)
		except Exception:
			return None
	elif group.name=='doctors_group':
		return HttpResponseRedirect('../../doctors/')
	elif user.is_superuser():
		return HttpResponseRedirect('../../administrators/')
	else:
		profile= None

