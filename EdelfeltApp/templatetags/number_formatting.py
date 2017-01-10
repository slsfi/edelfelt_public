__author__ = 'dennis'

from django import template
register = template.Library()

@register.filter
def float_to_percent(value):
    return value * 10