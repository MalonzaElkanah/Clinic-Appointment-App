from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def index(request):
	return render(request, 'cas/index.html')


def user_login(request):
	if request.user.is_authenticated:
		group = user.groups.get()
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


def privacy_policy(request):
	return render(request, 'cas/privacy-policy.html')


def term_condition(request):
	return render(request, 'cas/term-condition.html')
