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




@register.filter(name='is_complated_ap')
def ckeck_is_complated(status):
    return Appointment.COMPLETED == status


@register.filter(name='is_reschedule')
def ckeck_is_requested(status):
    return Appointment.RESCHEDULE_REQUESTED == status

@register.filter(name='is_canceled_ap')
def ckeck_is_canceled(status):
    return Appointment.CANCELED == status

@register.filter(name='is_created')
def ckeck_is_approved(status):
    return Appointment.CREATED == status.lower()

@register.filter(name='is_confirmed')
def ckeck_is_approved(status):
    return Appointment.CONFIRMED == status

