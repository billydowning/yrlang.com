from django.db import models

from users.models import CustomUser

# Create your models here.


class PaymentAccount(models.Model):
    CUR_US = 'USD'
    CURRENCIES = (
        (CUR_US, 'USD - United Stats (USA)'),
        (CUR_US, 'INR - India (IND)'),
    )

    CON_US = 'US'
    COUNTRIES = (
        (CON_US, 'US - United Stats (USA)'),
        (CON_US, 'IND - India (IND)'),
    )

    COMPANY = 'company'
    INDIVIDUAL = 'individual'
    HOLDER_TYPES = (
        (INDIVIDUAL, 'Individual Type'),
        (COMPANY, 'Company Type'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, default='bank_account')
    country = models.CharField(max_length=50, choices=COUNTRIES, default=CON_US)
    currency = models.CharField(max_length=50, choices=CURRENCIES, default=CUR_US)
    bank_name = models.CharField(max_length=50)
    routing_number = models.CharField(max_length=25, null=True, blank=True)
    account_number = models.CharField(max_length=25)
    account_holder_name = models.CharField(max_length=50)
    account_holder_type = models.CharField(choices=HOLDER_TYPES, default=INDIVIDUAL, max_length=30)
    account_id = models.CharField(max_length=255, null=True, blank=True)
    account_link = models.CharField(max_length=255, null=True, blank=True)
    account_status = models.CharField(max_length=255, null=True, blank=True)


    def __str__(self):
        return '{} - {}'.format(self.bank_name, self.currency)