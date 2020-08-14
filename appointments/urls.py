from django.urls import path

from . import views

urlpatterns = [
    path('request-appointment/<int:pk>', views.AppoitnemtRequestView.as_view(), name='request_appointment'),
    path('appointments', views.AppointmentView.as_view(), name="appointments"),
    path('new-appointment/<int:pk>', views.NewAppointmentView.as_view(), name="new_appointment"),
    path('edit-booking-request/', views.EditBookingRequestView.as_view(), name="edit_booking_appointment_request"),
    path('appointments-detail/<int:pk>', views.AppointmentDetailView.as_view(), name='appointments_detail'),
    path('provider-appointments-detail/<int:pk>', views.ProviderAppointmentDetailView.as_view(), name='provider_appointments_detail'),
    path('provider-request-appointment/<int:pk>', views.ProviderAppointmentCreateView.as_view(), name='create_provider_appointments'),
    path('provider-appointments/', views.ProviderAppointmentList.as_view(), name='provider_appointment'),
    path('edit-provider-appointment/<int:pk>', views.EditProviderAppointmentView.as_view(), name='edit_provider_appointment'),
    path('cancle-appointment/<int:pk>', views.CancelAppointmnetView.as_view(), name='cancel_appointment'),
    path('save-bookings/', views.SaveBookings.as_view(), name='save_bookings'),
    path('save-appointment/', views.SaveAppointments.as_view(), name='save_appointment'),
]
