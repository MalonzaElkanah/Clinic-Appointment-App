from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.decorators import login_required

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


@login_required(login_url='/login/')
def doctor_dashboard(request):
	return render(request, 'doctors/doctor-dashboard.html')


@login_required(login_url='/login/')
def doctor_profile_settings(request):
	return render(request, 'doctors/doctor-profile-settings.html')


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
	
