from django.db import models
from django.urls import reverse

from users.models import CustomUser


class Appointment(models.Model):
    CREATED = 'created'
    CONFIRMED = 'confirmed'
    RESCHEDULE_REQUESTED = 'rescheduled_requested'
    RESCHEDULE_ACCEPTED = 'rescheduled_accepted'
    WITH_PROVIDER = 'with_provider'
    WITH_CLIENT = 'with_client'
    COMPLETED = 'completed'
    CANCELED = 'canceled'

    STATUS_CHOICES = [
        (CONFIRMED, 'Confirmed'),
        (CANCELED, 'Canceled'),
        (CREATED, 'Request created (by Customer)'),
        (RESCHEDULE_REQUESTED, 'Reschedule Requested (by Customer)'),
        (RESCHEDULE_ACCEPTED, 'Reschedule Accepted (by Localite)'),
        (WITH_PROVIDER, 'Request accepted and Booking created (by Localite)'),
        (WITH_CLIENT, 'Request accepted by Customer (Final stage - means both Customer and Localite accepted Booking)'),
        (COMPLETED, 'Booking completed (by Localite)')
    ]

    date_created = models.DateTimeField(auto_now=True)
    requestor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="requestor")
    requestee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="requestee")
    customer_comment = models.TextField(null=True, blank=True)
    localite_comment = models.TextField(null=True, blank=True)
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

    def __str__(self):
        return '{} - {} - {}'.format(self.date, self.start_time, self.end_time)


class ProviderAppointment(models.Model):
    REQUESTED = 'requested'
    APPROVED = 'approved'
    CANCELED = 'canceled'
    COMPLETED = 'completed'
    THROUGH_PLATFORM = 'through_platform'
    OTHER_OPTIONS = 'other_options'

    STATUS_CHOICES = [
        (REQUESTED, 'Requested By Customer'),
        (APPROVED, 'Approved By Provider'),
        (CANCELED, 'Canceled By Provider'),
        (COMPLETED, 'Appointment Completed'),
    ]

    PAYMENT_METHODS_CHOICES = [
        (THROUGH_PLATFORM, 'Payment Through Platform'),
        (OTHER_OPTIONS, 'Other Payment Options'),
    ]

    requestor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='client')
    requestee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='provider')
    client_comment = models.TextField(null=True, blank=True)
    provider_comment = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=REQUESTED)
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS_CHOICES,
        default=THROUGH_PLATFORM
    )
    created_date = models.DateTimeField(auto_now=True)
    approved_date = models.DateTimeField(null=True, blank=True)
    request_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return '{} - {}'.format(self.requestor.username, self.requestee.username)

    def get_absolute_url(self):
        return reverse('provider_appointments_detail', args=[self.pk])
