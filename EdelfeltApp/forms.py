# coding=utf8
__author__ = 'dennis'
from haystack.forms import *
from django import forms
from django.utils.translation import ugettext_lazy as _

class CustomSearchForm(HighlightedModelSearchForm):
    q = forms.CharField(required=False, label='Sök efter ett eller flera ord, även partiella träffar beaktas:',
                        widget=forms.widgets.TextInput(attrs={"class":"form-control", "placeholder":"Sök i materialet"}))
    models = forms.MultipleChoiceField(choices=model_choices(), required=False,
                                       label='Sök efter', widget=forms.CheckboxSelectMultiple)
