from django import template
from django.db.models import Q
from main.models import ReportAProblem

register = template.Library()


@register.filter(name='is_complain_solved')
def is_complain_solved(status):
    return status == ReportAProblem.SOLEVE


@register.filter(name='is_complain_unsolved')
def is_complain_solved(status):
    return status == ReportAProblem.UNSOLVE
