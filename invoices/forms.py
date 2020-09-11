from django.forms import ModelForm, Form
from django import forms


from .models import Invoice
from users.models import CustomUser
from appointments.models import Appointment, ProviderAppointment


class CreateInvoiceForm(ModelForm):
	booking = forms.ModelChoiceField(queryset=Appointment.objects.all())
	class Meta:
		model=Invoice
		fields=["title","amount", "booking"]

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super(CreateInvoiceForm, self).__init__(*args, **kwargs)
		self.fields['booking'].queryset = Appointment.objects.filter(
			requestee=self.user,
			status=Appointment.CONFIRMED or Appointment.COMPLETED
		)


class ProviderCreateInvoiceForm(ModelForm):
	appointment = forms.ModelChoiceField(queryset=ProviderAppointment.objects.filter())
	class Meta:
		model=Invoice
		fields=["title","amount", "appointment"]

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super(ProviderCreateInvoiceForm, self).__init__(*args, **kwargs)
		self.fields['appointment'].queryset = ProviderAppointment.objects.filter(
			requestee=self.user,
			status=ProviderAppointment.APPROVED or ProviderAppointment.COMPLETED
		)