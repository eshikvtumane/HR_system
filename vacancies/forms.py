#-*- coding: utf8 -*-
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.forms import ModelForm
from vacancies.models import Vacancy,Department,Status
from applicants.models import Position


class AddVacancyForm(ModelForm):

    class Meta:
        model = Vacancy
        fields = ("salary","end_date","description",'head','position')
        labels = {
            'salary': _(u'Зарплата'),
            'end_date': _(u'Предполагамый срок закрытия'),
            'description': _(u'Описание'),

        }
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

            }),
            'position':forms.Select(attrs={'class':'form-control','id':'position'})
        }



class EditVacancyForm(ModelForm):

   class Meta:
        model = Vacancy
        fields = ("salary","end_date","description",'position','status')
        labels = {
            'salary': _(u'Зарплата'),
            'end_date': _(u'Предполагамый срок закрытия'),
            'description': _(u'Описание'),

        }
        widgets = {
            'salary': forms.NumberInput(attrs={
                'class': "form-control",
                'name':'salary'
            }),
            'end_date': forms.DateInput(format=('%d-%m-%Y'),attrs={
                'id':'end_date',
                'class': "form-control",
                'name':'end_date',
                'data-validation': "date",
                'data-validation-format': "dd-mm-yyyy"

            }),
            'description':forms.Textarea(attrs={
                'class':'form-control'


            }),

            'status':forms.Select(attrs={'class':'form-control','id':'status'})


        }


