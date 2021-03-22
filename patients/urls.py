from django.urls import path

from . import views

urlpatterns = [
 	path('register/', views.register, name='register'),
 	path('profile-settings/', views.profile_settings, name='profile-settings'),
	path('', views.patient_dashboard, name='patient-dashboard'),
 	path('doctor-profile/<slug:slug>/<int:doctor_id>/', views.doctor_profile, name='doctor-profile'),
	path('booking/<slug:slug>/<int:doctor_id>/', views.booking, name='booking'),
 	path('checkout/', views.checkout, name='checkout'),
 	path('booking-success/', views.booking_success, name='booking-success'),
 	path('invoice-view/<slug:slug>/<int:invoice_id>/', views.invoice_view, name='invoice-view'),
 	path('favourites/', views.favourites, name='favourites'),
 	path('favourite-doctor/<slug:slug>/<int:doctor_id>/', views.favourite_doctor, name='favourite-doctor'),
	path('change-password/', views.change_password, name='change-password'),
	
 	path('chat/', views.chat, name='chat'),
 	#path('test/', views.test, name='test'),
]