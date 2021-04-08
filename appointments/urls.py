from django.urls import path

from . import views

urlpatterns = [
	# Doctor URLS
	path('doctors/', views.doctor_dashboard, name='doctor-dashboard'),
	path('doctors/register/', views.doctor_register, name='doctor-register'),
	path('doctors/profile-settings/', views.doctor_profile_settings, name='doctor-profile-settings'),
	path('doctors/profile/settings-page2/', views.doctor_profile_page2, name='doctor-profile-page2'),
	path('doctors/appointments/', views.appointments, name='appointments'),
	path('doctors/appointment/<slug:slug>/accept/<int:appointment_id>/', views.appointment_accept, 
		name='appointment-accept'),
	path('doctors/appointment/<slug:slug>/cancel/<int:appointment_id>/', views.appointment_cancel, 
		name='appointment-cancel'),
	path('doctors/appointment/<slug:slug>/complete/<int:appointment_id>/', views.appointment_complete, 
		name='appointment-complete'),
	path('doctors/my-patients/', views.my_patients,  name='my-patients'),
	path('doctors/schedule-timings/', views.schedule_timings, name='schedule-timings'),
	path('doctors/timeslot/new/', views.new_timeslot, name='new-timeslot'),
	path('doctors/timeslot/update/', views.update_timeslot, name='update-timeslot'),
	path('doctors/timeslot/delete/<slug:slug>/<int:slot_id>/', views.delete_timeslot, name='delete-timeslot'),
	path('doctors/invoices/', views.invoices, name='invoices'),
	path('doctors/invoice/<slug:slug>/<int:invoice_id>/', views.invoice, name='invoice'),
	path('invoice-pdf/<slug:slug>/<int:invoice_id>/', views.invoice_pdf, name='invoice-pdf'),
	path('doctors/reviews/', views.reviews, name='reviews'),
	path('doctors/social-media/', views.social_media, name = 'social-media'),
	path('doctors/change-password/', views.doctor_change_password, name='doctor-change-password'),
	path('doctors/patient-profile/<slug:slug>/<int:patient_id>/', views.patient_profile, 
		name='patient-profile'),
	path('doctors/add-prescription/<slug:slug>/<int:patient_id>/', views.add_prescription, 
		name='add-prescription'),
	path('doctors/edit-prescription/<int:patient_id>/<slug:slug>/<int:prescription_id>/', 
		views.edit_prescription, name='edit-prescription'),
	path('doctors/add-billing/<slug:slug>/<int:patient_id>/<int:appointment_id>/', views.add_billing,  
		name='add-billing'),
	path('doctors/edit-billing/<slug:slug>/<int:patient_id>/', views.edit_billing, name='edit-billing'),
	path('doctors/chat-doctor/', views.chat_doctor, name='chat-doctor'),

	# Patient URLS
	path('patients/register/', views.register, name='register'),
 	path('patients/profile-settings/', views.profile_settings, name='profile-settings'),
	path('patients/', views.patient_dashboard, name='patient-dashboard'),
	
 	path('doctor-profile/<slug:slug>/<int:doctor_id>/', views.doctor_profile, name='doctor-profile'),
	path('booking/<slug:slug>/<int:doctor_id>/', views.booking, name='booking'),
 	path('patients/checkout/', views.checkout, name='checkout'),
 	path('patients/booking-success/', views.booking_success, name='booking-success'),
 	path('patients/invoice-view/<slug:slug>/<int:invoice_id>/', views.invoice_view, name='invoice-view'),
 	path('patients/favourites/', views.favourites, name='favourites'),
 	path('patients/favourite-doctor/<slug:slug>/<int:doctor_id>/', views.favourite_doctor, 
 		name='favourite-doctor'),
	path('patients/change-password/', views.change_password, name='change-password'),
	
	path('patients/add-review/', views.add_review, name='add-review'),
 	path('patients/chat/', views.chat, name='chat'),
]