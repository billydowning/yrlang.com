from django import template
from appointments.models import Appointment, ProviderAppointment
from django.contrib.contenttypes.models import ContentType
from main.models import ReportAProblem

register = template.Library()


@register.simple_tag(name='check_appointment_complain')
def check_appointment_complain(user,appointment_id):
    content_type = ContentType.objects.get_for_model(ProviderAppointment)
    flag = ReportAProblem.objects.filter(content_type=content_type, object_id= appointment_id, reporter= user).exists()
    return flag

@register.simple_tag(name='check_booking_complain')
def check_booking_complain(user,booking_id):
    content_type = ContentType.objects.get_for_model(Appointment)
    flag = ReportAProblem.objects.filter(content_type=content_type, object_id= booking_id, reporter= user).exists()
    return flag
