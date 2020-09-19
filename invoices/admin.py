from django.contrib import admin
from .models import Invoice, MonthlySubscriptionInvoice, MonthlyProviderAppointmentCount


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('title', '__str__', 'date_created', 'amount','payee', 'payor')
    list_display_links = ('__str__',)
    list_per_page = 25
    search_fields = ['email', 'language', 'country', 'state']


admin.site.register(Invoice, InvoiceAdmin)


class MonthlyProviderAppointmentCountInline(admin.TabularInline):
    model = MonthlyProviderAppointmentCount
    can_delete = True
    extra = 0
    classes = ['collapse', ]
    verbose_name = 'Count'
    verbose_name_plural = 'Counts'


class MonthlySubscriptionInvoiceAdmin(admin.ModelAdmin):
    inlines = [MonthlyProviderAppointmentCountInline,]


admin.site.register(MonthlySubscriptionInvoice, MonthlySubscriptionInvoiceAdmin)
