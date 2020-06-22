from django.forms import ModelForm, Form
from django import forms
from .models import Invoice
from users.models import CustomUser

class CreateInvoiceForm(ModelForm):
	payor = forms.ModelChoiceField(queryset=CustomUser.objects.all())
	class Meta:
		model=Invoice
		fields=["title","amount"]