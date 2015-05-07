#-*- coding: utf8 -*-
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.forms import ModelForm
from applicants.models import Position

class EmailPositionForm(forms.Form):

    position = forms.ModelChoiceField(queryset=Position.objects.all(),
                                   widget=forms.Select(attrs={
                                     'class':'select',
                                     'placeholder':'Должности'
                                   })
                                   )