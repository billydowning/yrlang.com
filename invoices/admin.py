from django.contrib import admin
from .models import Invoice


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('title', '__str__', 'date_created', 'amount','payee', 'payor')
    list_display_links = ('__str__',)
    list_per_page = 25
    search_fields = ['email', 'language', 'country', 'state']


admin.site.register(Invoice, InvoiceAdmin)
