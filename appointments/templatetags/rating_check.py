from django import template
from django.db.models import Q
from appointments.models import Appointment, ProviderAppointment
from django.contrib.contenttypes.models import ContentType
from main.models import Review

register = template.Library()


@register.simple_tag(name='check_appointment_rating')
def check_booking_rating(user,appointment_id):
    content_type = ContentType.objects.get_for_model(ProviderAppointment)
    flag = Review.objects.filter(content_type=content_type, object_id= appointment_id, reviewer= user).exists()
    return flag

@register.simple_tag(name='check_booking_rating')
def check_booking_rating(user,booking_id):
    content_type = ContentType.objects.get_for_model(Appointment)
    flag = Review.objects.filter(content_type=content_type, object_id= booking_id, reviewer= user).exists()
    return flag

@register.filter
def classname(obj):
    return obj.__class__.__name__
