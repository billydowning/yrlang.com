from django.forms import ModelForm, Form
from django import forms
from django.shortcuts import get_object_or_404

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
		self.object_id  =  kwargs.pop("object_id",None)
		super(CreateInvoiceForm, self).__init__(*args, **kwargs)
		if self.object_id:
			obj =get_object_or_404(Appointment, pk=self.object_id)
			self.fields['booking'].initial = obj
			self.fields['booking'].widget = forms.HiddenInput()
			self.fields['booking'].label = ""
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
		self.object_id = kwargs.pop("object_id", None)
		super(ProviderCreateInvoiceForm, self).__init__(*args, **kwargs)
		if self.object_id:
			obj =get_object_or_404(ProviderAppointment, pk=self.object_id)
			self.fields['appointment'].initial = obj
			self.fields['appointment'].widget = forms.HiddenInput()
			self.fields['appointment'].label = ""
		self.fields['appointment'].queryset = ProviderAppointment.objects.filter(
			requestee=self.user,
			status=ProviderAppointment.APPROVED or ProviderAppointment.COMPLETED
		)