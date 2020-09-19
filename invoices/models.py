from datetime import datetime

from django.db import models
from django.urls import reverse

from appointments.models import Appointment, ProviderAppointment
from users.models import CustomUser


class Invoice(models.Model):
    title = models.CharField(max_length=100)
    date_created = models.DateField(auto_now=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    currency = models.CharField(max_length=10, default='USD')
    is_paid = models.BooleanField(default=False)
    date_paid = models.DateField(blank=True, null=True)
    payee = models.ForeignKey(CustomUser, blank=True, null=True, related_name="payee", on_delete=models.CASCADE)
    payor = models.ForeignKey(CustomUser, blank=True, null=True, related_name="payor", on_delete=models.CASCADE)
    stripe_payment_id = models.CharField(max_length=150, blank=True, null=True)
    booking = models.ForeignKey(Appointment, on_delete=models.CASCADE, blank=True, null=True)
    appointment = models.ForeignKey(ProviderAppointment, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.id)

    def get_invoice_absolute_url(self):
        return reverse('custom_admin:invoice', args=[self.pk])


class MonthlySubscriptionInvoice(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    amount = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    currency = models.CharField(max_length=10, default='USD')
    is_paid = models.BooleanField(default=False)
    date_paid = models.DateTimeField(blank=True, null=True)
    provider = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    stripe_payment_id = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title = str(datetime.now().year) + ' ' + datetime.now().strftime("%B")
        super(MonthlySubscriptionInvoice, self).save(*args, **kwargs)


class MonthlyProviderAppointmentCount(models.Model):
    invoice = models.ForeignKey(MonthlySubscriptionInvoice, on_delete=models.CASCADE, related_name='appointment_count')
    provider = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='provider_count')
    appointment = models.ForeignKey(ProviderAppointment, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['provider', 'appointment']

    def __str__(self):
        return self.provider.email
