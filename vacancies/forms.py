#-*- coding: utf8 -*-

from django import forms
from django.forms import ModelForm
from vacancies.models import Vacancy,Department
from applicants.models import Position


class VacancyForm(ModelForm):

    position = forms.ModelChoiceField(queryset=Position.objects.all(),
                                       label='Должность',
                                       widget=forms.Select(attrs={
                                           'class':'',
                                           'placeholder':'Выберите должность'
                                       }
                                       )
                                 )
    class Meta:
        model = Vacancy
        fields = ("position","salary","end_date","description")
        widgets = {
            'salary': forms.NumberInput(attrs={
                'class': "form-control",
                'name':'salary'
            }),
            'end_date': forms.DateInput(attrs={
                'id':'end_date',
                'class': "form-control",
                'name':'end_date',
                'data-validation': "date",
                'data-validation-format': "dd-mm-yyyy"

            }),
            'description':forms.Textarea(attrs={
                'class':'form-control'

            })
        }




