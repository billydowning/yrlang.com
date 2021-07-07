from django.forms import ModelForm, Form

from .models import PaymentAccount


class PaymentAccountForm(ModelForm):

    class Meta:
        model = PaymentAccount
        fields = [
            'bank_name',
            'country',
            'currency',
            'account_holder_name',
            'account_number',
            'account_holder_type',
        ]