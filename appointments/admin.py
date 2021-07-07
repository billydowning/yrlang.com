from django.contrib import admin

from .models import Appointment, ProviderAppointment, BookingDates
# Register your models here.


class BookingDatesInline(admin.TabularInline):
    model = BookingDates
    fk_name = 'booking'
    can_delete = True
    extra = 0
    verbose_name_plural = 'Booking Dates'


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'date_created', "status" )
    list_display_links = ('__str__', )
    list_filter = ('requestee', 'requestor', 'date_created')
    list_per_page = 25
    search_fields = ['requestee', 'requestor', ]
    inlines = [BookingDatesInline]


admin.site.register(Appointment, AppointmentAdmin)


admin.site.register(ProviderAppointment)

