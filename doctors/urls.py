from django.urls import path

from . import views

urlpatterns = [
	path('', views.doctor_dashboard, name='doctor-dashboard'),
	path('register/', views.doctor_register, name='doctor-register'),
	path('profile-settings/', views.doctor_profile_settings, name='doctor-profile-settings'),
	path('profile/settings-page2/', views.doctor_profile_page2, name='doctor-profile-page2'),
	path('schedule-timings/', views.schedule_timings, name='schedule-timings'),
	path('timeslot/new/', views.new_timeslot, name='new-timeslot'),
	path('timeslot/update/', views.update_timeslot, name='update-timeslot'),
	path('timeslot/delete/<slug:slug>/<int:slot_id>/', views.delete_timeslot, name='delete-timeslot'),
	path('social-media/', views.social_media, name = 'social-media'),
	
	path('my-patients/', views.my_patients,  name='my-patients'),
	path('add-billing/', views.add_billing,  name='add-billing'),
	path('reviews/', views.reviews, name='reviews'),
	path('edit-billing/', views.edit_billing, name='edit-billing'),
	path('add-prescription/', views.add_prescription, name='add-prescription'),
	path('change-password/', views.doctor_change_password, name='doctor-change-password'),
	path('chat-doctor/', views.chat_doctor, name='chat-doctor'),
	path('patient-profile/', views.patient_profile, name='patient-profile'),
	path('invoices/', views.invoices, name='invoices'),
	path('appointments/', views.appointments, name='appointments'),
	path('edit-prescription/', views.edit_prescription, name='edit-prescription'),
]