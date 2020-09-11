from django.contrib import admin

from .models import PaymentAccount, Commission, StripeKeys

# Register your models here.


admin.site.register(PaymentAccount)
admin.site.register(Commission)
admin.site.register(StripeKeys)
