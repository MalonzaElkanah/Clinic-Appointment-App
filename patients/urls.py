from django.urls import path

from . import views

urlpatterns = [
 	path('register/', views.register, name='register'),
	path('', views.patient_dashboard, name='patient-dashboard'),
	path('booking/', views.booking, name='booking'),
 	path('booking-success/', views.booking_success, name='booking-success'),
 	path('checkout/', views.checkout, name='checkout'),
 	path('change-password/', views.change_password, name='change-password'),
 	path('doctor-profile/', views.doctor_profile, name='doctor-profile'),
 	path('profile-settings/', views.profile_settings, name='profile-settings'),
 	path('chat/', views.chat, name='chat'),
 	path('invoice-view/', views.invoice_view, name='invoice-view'),
 	path('favourites/', views.favourites, name='favourites'),
]