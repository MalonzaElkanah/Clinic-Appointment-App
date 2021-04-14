from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from appointments.models import Speciality, Doctor, Patient
from administrators.models import Admin


def get_profile(user):
	if user.is_authenticated:
		profile = None
		try:
			group = user.groups.get()
			if group.name=='patients_group':
				profile = Patient.objects.get(user=user.id)
			elif group.name=='doctors_group':
				profile = Doctor.objects.get(user=user.id)
			elif user.is_superuser:
				profile = Admin.objects.get(user=user.id)
			else:
				return profile
			return profile
		except Exception:
			if user.is_superuser:
				profile = Admin.objects.get(user=user.id)
			return profile
	else:
		return None


def index(request):
	specialities = Speciality.objects.all()
	doctors = Doctor.objects.all()
	profile = get_profile(request.user)
	return render(request, 'cas/index.html', {"specialities": specialities, "doctors": doctors, 
		"profile": profile})


def user_login(request):
	if request.user.is_authenticated:
		group = request.user.groups.get()
		if group.name=='patients_group':
			return HttpResponseRedirect('../patients/')
		elif group.name=='doctors_group':
			return HttpResponseRedirect('../doctors/')
		elif user.is_superuser():
			return HttpResponseRedirect('../administrators/')
		else:
			return HttpResponseRedirect('../')
	elif request.is_ajax():
		user = authenticate(username=request.POST['email'], password=request.POST['password'])
		if user is not None:
			login(request, user)
			user = User.objects.get(username=request.POST['email'])

			try:
				return HttpResponseRedirect(''+request.POST['next'])
			except Exception:
				group_set = user.groups.all()
				redirect = "../"
				for my_group in group_set:
					if my_group.name == 'doctors_group':
						redirect = '../doctors/'
					elif my_group.name == 'patients_group':
						redirect = '../patients/'
				if user.is_superuser:
					redirect = '../../administrators/'
				return JsonResponse({"success": "User Logged In.", 
					"redirect": redirect}, status=200)
		else:
			return JsonResponse({"error": "Error: username and password do not match."}, 
				status=200) 

	elif request.method == 'GET':
		try:
			return render(request, 'registration/login.html', {'next': request.GET['next']})
		except Exception:
			return render(request, 'cas/login.html')
	else:
		return render(request, 'cas/login.html')


@login_required(login_url='/login/')
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('../login/')


def search_results(request):
	if request.method == 'GET':
		profile = get_profile(request.user)
		doctors = {}
		word = request.GET['search']
		loc = request.GET['location']
		if word == '' and not loc == '':
			doctors = Doctor.objects.filter(Q(address_line1__contains=loc) | Q(address_line2__contains=loc) | Q(country__contains=loc) | Q(county__contains=loc) | Q(town__contains=loc) | Q(clinic__contains=loc) | Q(clinic_address__contains=loc))
		elif not word == '' and loc == '':
			doctors = Doctor.objects.filter(Q(first_name__contains=word) | Q(second_name__contains=word) | Q(services__contains=word) | Q(specialization__contains=word) | Q(clinic__contains=word))
		elif not word == '' and not loc == '':
			query = Doctor.objects.filter(Q(address_line1__contains=loc) | Q(address_line2__contains=loc) | Q(country__contains=loc) | Q(county__contains=loc) | Q(town__contains=loc) | Q(clinic__contains=loc) | Q(clinic_address__contains=loc))
			doctors = query.filter(Q(first_name__contains=word) | Q(second_name__contains=word) | Q(services__contains=word) | Q(specialization__contains=word) | Q(clinic__contains=word))
		elif word == '' and loc == '':
			doctors == {}
		else:
			query = Doctor.objects.filter(Q(address_line1__contains=loc) | Q(address_line2__contains=loc) | Q(country__contains=loc) | Q(county__contains=loc) | Q(town__contains=loc) | Q(clinic__contains=loc) | Q(clinic_address__contains=loc))
			doctors = query.filter(Q(first_name__contains=word) | Q(second_name__contains=word) | Q(services__contains=word) | Q(specialization__contains=word) | Q(clinic__contains=word))
		
		specialities = Speciality.objects.all()
		return render(request, 'cas/search.html', {'doctors': doctors, 'keyword': word, 'location': loc, 
			'profile': profile, 'specialities': specialities})



def privacy_policy(request):
	return render(request, 'cas/privacy-policy.html')


def term_condition(request):
	return render(request, 'cas/term-condition.html')
