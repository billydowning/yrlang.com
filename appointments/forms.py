from datetime import datetime

from django.forms import ModelForm, Form
from django import forms

from .models import Appointment, ProviderAppointment
from invoices.models import MonthlySubscriptionInvoice, MonthlyProviderAppointmentCount


# class AppointmentForm(ModelForm):
#
#     class Meta:
#         model = Appointment
#         fields = [
#             "requested_date_1", 'requested_date_1_start_time', 'requested_date_1_end_time',
#             "requested_date_2", 'requested_date_2_start_time', 'requested_date_2_end_time'
#         ]
#         labels = {
#             'requested_date_1': 'Day 1 Date',
#             'requested_date_1_start_time': 'Start Time',
#             'requested_date_1_end_time': 'End Time',
#             'requested_date_2': 'Day 2 Date',
#             'requested_date_2_start_time': 'Start Time',
#             'requested_date_2_end_time': 'End Time'
#         }
#
#     def __init__(self, *args, **kwargs):
#         super(AppointmentForm, self).__init__(*args, **kwargs)
#         self.fields['requested_date_1'].required = True
#         self.fields['requested_date_2'].required = False
#         for field in self.fields:
#             self.fields[field].widget.attrs.update({
#                 'autocomplete': 'off', 'readonly': True
#             })


# class NewAppointmentForm(ModelForm):
#     class Meta:
#         model = Appointment
#         fields = ["start_time", "end_time", "notes"]
#
#     def __init__(self, *args, **kwargs):
#         super(NewAppointmentForm, self).__init__(*args, **kwargs)
#         self.fields['start_time'].widget.attrs.update({
#             'autocomplete': 'off', })
#         self.fields['end_time'].widget.attrs.update({
#             'autocomplete': 'off', })


class ProviderAppointmentCreateForm(ModelForm):
    class Meta:
        model = ProviderAppointment
        fields = ["request_date", "client_comment", ]

    def __init__(self, *args, **kwargs):
        super(ProviderAppointmentCreateForm, self).__init__(*args, **kwargs)
        self.fields['request_date'].required = True


class ApproveProviderAppointmentForm(ModelForm):
    status = forms.BooleanField(
        widget=forms.HiddenInput(),
        initial=False
    )

    class Meta:
        model = ProviderAppointment
        fields = ['approved_date', 'provider_comment']

    def __init__(self, *args, **kwargs):
        super(ApproveProviderAppointmentForm, self).__init__(*args, **kwargs)
        self.fields['status'].required = False
        self.fields['approved_date'].required = False
        self.fields['provider_comment'].required = False

    def save(self, commit=True):
        instance = super(ApproveProviderAppointmentForm, self).save()
        status = self.cleaned_data['status']
        if status:
            instance.status = ProviderAppointment.APPROVED
            invoice = self.get_invoice(instance.requestee)
            if invoice:
                if not MonthlyProviderAppointmentCount.objects.filter(
                    provider=instance.requestee,
                    appointment=instance,
                    invoice=invoice
                ).exists():
                    try:
                        MonthlyProviderAppointmentCount.objects.create(
                            provider=instance.requestee,
                            appointment=instance,
                            invoice=invoice
                        )
                    except Exception as e:
                        print(e)
        elif not status:
            instance.status = ProviderAppointment.CANCELED
        instance.save()
        return instance

    def get_invoice(self, provider):
        try:
            obj, _ = MonthlySubscriptionInvoice.objects.get_or_create(
                provider=provider,
                date_created__month=datetime.now().month,
                date_created__year=datetime.now().year
            )
        except Exception as e:
            print(e)
        return obj
