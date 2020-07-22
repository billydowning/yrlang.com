from django import template
from django.db.models import Q
from users.models import UserRole, UserRoleRequest
from datetime import date
from dateutil.relativedelta import relativedelta

six_months = date.today() + relativedelta(months=+6)

register = template.Library()


@register.filter(name='request_localite')
def request_for_localite(name):
    return UserRole.LOCALITE == name


@register.filter(name='request_provider')
def request_for_provider(name):
    return UserRole.PROVIDER == name


@register.simple_tag(name='provider_request_sent')
def check_is_client(user):
    user_req_status = user.request_user.all().filter(requested_for__name=UserRole.PROVIDER).order_by('-requested_on')
    flag = user_req_status.exists()
    if flag and user_req_status.first().requested_on.date() + relativedelta(months=+6) == date.today():
        flag = False
    return flag


@register.simple_tag(name='localite_request_sent')
def check_is_client(user):
    user_req_status = user.request_user.all().filter(requested_for__name=UserRole.LOCALITE).order_by('-requested_on')
    flag = user_req_status.exists()
    if flag and user_req_status.first().requested_on.date() + relativedelta(months=+6) == date.today():
        flag = False
    return flag


@register.simple_tag(name='lang_verifier_request_sent')
def check_is_client(user):
    user_req_status = user.request_user.all().filter(requested_for__name=UserRole.LANGUAGE_VERIFIER).order_by('-requested_on')
    flag = user_req_status.exists()
    if flag and user_req_status.first().requested_on.date()+ relativedelta(months=+6) == date.today():
        flag = False
    return flag
