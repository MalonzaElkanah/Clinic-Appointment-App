from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
	return render(request, 'cas/index.html')


def login(request):
	return render(request, 'cas/login.html')


def privacy_policy(request):
	return render(request, 'cas/privacy-policy.html')


def term_condition(request):
	return render(request, 'cas/term-condition.html')
