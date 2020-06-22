from django.db import models
from django.urls import reverse

from users.models import CustomUser


class Appointment(models.Model):
    CREATED = 'created'
    CONFIRMED = 'confirmed'
    RESCHEDULE_REQUESTED = 'rescheduled_requested'
    WITH_PROVIDER = 'with_provider'
    WITH_CLIENT = 'with_client'
    COMPLETED = 'completed'
    CANCELED = 'canceled'

    STATUS_CHOICES = [
        (CONFIRMED, 'Confirmed'),
        (CANCELED, 'Canceled'),
        (CREATED, 'Request created (by client)'),
        (RESCHEDULE_REQUESTED, 'Reschedule Requested (by client or provider)'),
        (WITH_PROVIDER, 'Request accepted and appointment created (by provider)'),
        (WITH_CLIENT, 'Request accepted by client (Final stage - means both client and provider accepted appointment)'),
        (COMPLETED, 'Appointment completed (by provider)')
    ]

    date_created = models.DateTimeField(auto_now=True)
    requestor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="requestor")
    requestee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="requestee")
    notes = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default=CREATED)

    def __str__(self):
        return '{} - {} - {}'.format(self.requestor.username, self.requestee.username, self.status)

    def get_absolute_url(self):
        return reverse('appointments_detail', args=[self.pk])


class BookingDates(models.Model):
    booking = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='booking')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    confirmed = models.BooleanField(default=False)


class ProviderAppointment(models.Model):
    REQUESTED = 'requested'
    APPROVED = 'approved'
    CANCELED = 'canceled'
    COMPLETED = 'completed'

    STATUS_CHOICES = [
        (REQUESTED, 'Requested By Customer'),
        (APPROVED, 'Approved By Provider'),
        (CANCELED, 'Canceled By Provider'),
        (COMPLETED, 'Appointment Completed'),
    ]

    requestor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='client')
    requestee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='provider')
    client_comment = models.TextField(null=True, blank=True)
    provider_comment = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=REQUESTED)
    created_date = models.DateTimeField(auto_now=True)
    approved_date = models.DateTimeField(null=True, blank=True)
    request_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return '{} - {}'.format(self.requestor.username, self.requestee.username)

    def get_absolute_url(self):
        return reverse('provider_appointments_detail', args=[self.pk])
