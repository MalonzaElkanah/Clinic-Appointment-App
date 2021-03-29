from django.urls import path

from . import views

urlpatterns = [
	path('', views.doctor_dashboard, name='doctor-dashboard'),
	path('register/', views.doctor_register, name='doctor-register'),
	path('profile-settings/', views.doctor_profile_settings, name='doctor-profile-settings'),
	path('profile/settings-page2/', views.doctor_profile_page2, name='doctor-profile-page2'),
	path('appointments/', views.appointments, name='appointments'),
	path('appointment/<slug:slug>/accept/<int:appointment_id>/', views.appointment_accept, 
		name='appointment-accept'),
	path('appointment/<slug:slug>/cancel/<int:appointment_id>/', views.appointment_cancel, 
		name='appointment-cancel'),
	path('appointment/<slug:slug>/complete/<int:appointment_id>/', views.appointment_complete, 
		name='appointment-complete'),
	path('my-patients/', views.my_patients,  name='my-patients'),
	path('schedule-timings/', views.schedule_timings, name='schedule-timings'),
	path('timeslot/new/', views.new_timeslot, name='new-timeslot'),
	path('timeslot/update/', views.update_timeslot, name='update-timeslot'),
	path('timeslot/delete/<slug:slug>/<int:slot_id>/', views.delete_timeslot, name='delete-timeslot'),
	path('invoices/', views.invoices, name='invoices'),
	path('invoice/<slug:slug>/<int:invoice_id>/', views.invoice, name='invoice'),
	path('reviews/', views.reviews, name='reviews'),
	path('social-media/', views.social_media, name = 'social-media'),
	path('change-password/', views.doctor_change_password, name='doctor-change-password'),
	
	path('patient-profile/<slug:slug>/<int:patient_id>/', views.patient_profile, name='patient-profile'),
	path('add-prescription/<slug:slug>/<int:patient_id>/', views.add_prescription, name='add-prescription'),
	path('edit-prescription/<int:patient_id>/<slug:slug>/<int:prescription_id>/', views.edit_prescription, 
		name='edit-prescription'),
	path('add-billing/<slug:slug>/<int:patient_id>/<int:appointment_id>/', views.add_billing,  
		name='add-billing'),
	path('edit-billing/<slug:slug>/<int:patient_id>/', views.edit_billing, name='edit-billing'),
	path('chat-doctor/', views.chat_doctor, name='chat-doctor'),
]