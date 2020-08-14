from datetime import datetime, timedelta

from django import template

from appointments.models import ProviderAppointment, Appointment

register = template.Library()


@register.filter(name='is_complated')
def ckeck_is_complated(status):
    return ProviderAppointment.COMPLETED == status


@register.filter(name='is_requested')
def ckeck_is_requested(status):
    return ProviderAppointment.REQUESTED == status

@register.filter(name='is_canceled')
def ckeck_is_canceled(status):
    return ProviderAppointment.CANCELED == status

@register.filter(name='is_approved')
def ckeck_is_approved(status):
    return ProviderAppointment.APPROVED == status


@register.filter(name='is_completed')
def ckeck_is_complated(status):
    return Appointment.COMPLETED == status


@register.filter(name='is_reschedule')
def ckeck_is_requested(status):
    return Appointment.RESCHEDULE_REQUESTED == status


@register.filter(name='is_canceled')
def ckeck_is_canceled(status):
    return Appointment.CANCELED == status


@register.filter(name='is_created')
def ckeck_is_approved(status):
    return Appointment.CREATED == status.lower()


@register.filter(name='is_confirmed')
def ckeck_is_approved(status):
    return Appointment.CONFIRMED == status


@register.filter(name='is_rescheduled_requested')
def check_is_rescheduled_requested(status):
    return Appointment.RESCHEDULE_REQUESTED == status


@register.filter(name='is_rescheduled_accepted')
def check_is_rescheduled_requested(status):
    return Appointment.RESCHEDULE_REQUESTED == status


@register.filter(name='is_rescheduled_check')
def check_is_rescheduled_check(booking):
    obj = booking.booking.all().order_by('start_time').order_by('date')[0]
    date = datetime.combine(obj.date, obj.start_time) - timedelta(hours=24)
    if datetime.now() > date:
        return False
    else:
        return True


