from django import template
from appointments.models import Appointment, ProviderAppointment
from django.contrib.contenttypes.models import ContentType
from main.models import ReportAProblem

register = template.Library()


@register.filter(name='is_img_type')
def check_is_img_type(img_type):
    img_type_list = ['.jpg','.png']
    if img_type in img_type_list:
        return True
    else:
        return False
