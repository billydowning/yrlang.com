from django.db import models

from users.models import CustomUser

# Create your models here.


class PaymentAccount(models.Model):
    COMPANY = 'company'
    INDIVIDUAL = 'individual'
    HOLDER_TYPES = (
        (INDIVIDUAL, 'Individual Type'),
        (COMPANY, 'Company Type'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, default='bank_account')
    country = models.CharField(max_length=50)
    currency = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=50)
    account_number = models.CharField(max_length=25)
    account_holder_name = models.CharField(max_length=50)
    account_holder_type = models.CharField(choices=HOLDER_TYPES, default=INDIVIDUAL, max_length=30)

    def __str__(self):
        return '{} - {}'.format(self.bank_name, self.currency)