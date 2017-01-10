__author__ = 'dennis'
from django import template
from EdelfeltApp.models import *
from django.core.urlresolvers import reverse
import re

register = template.Library()

@register.filter
def find_anchors(value):
    #needs to be done in a way that doesn't loop through all persons
    # for person in Person.objects.all():
    #     name = person.name()
    #     if name in value:
    #         value = re.sub(str(name), '<a href="foobar">' + name + '</a>', value)
    #         print value
    return value