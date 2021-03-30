from django.urls import path

from . import views

urlpatterns = [
	path('', views.admin_dashboard, name='admin-dashboard'),
	path('appointment-list/', views.appointment_list, name='appointment-list'),
	path('specialities/', views.specialities, name='specialities'),
	path('edit-speciality/', views.edit_speciality, name='edit-speciality'),
	path('delete-speciality/', views.delete_speciality, name='delete-speciality'),
	path('doctor-list/', views.doctor_list, name='doctor-list'),
	path('patient-list/', views.patient_list, name='patient-list'),
	path('reviews/', views.reviews, name='admin-reviews'),
	path('transactions-list/', views.transactions_list, name='transactions-list'),
	path('settings/', views.settings, name='settings'),
	path('invoice-report/', views.invoice_report, name='invoice-report'),
	path('profile/', views.profile, name='profile'),
	path('lock-screen/', views.lock_screen, name='lock-screen'),

	path('invoice/', views.invoice, name='invoice'),
	path('forgot-password/', views.forgot_password, name='forgot-password'),
]