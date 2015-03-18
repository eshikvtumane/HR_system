#-*- coding: utf8 -*-
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.forms import ModelForm
from vacancies.models import Vacancy,Department,Status
from applicants.models import Position


class VacancyForm(ModelForm):

    position = forms.ModelChoiceField(queryset=Position.objects.all(),
                                       label=u'Должность',
                                       widget=forms.Select(attrs={
                                           'class':'form-control',
                                           'placeholder':'Выберите должность'
                                       }
                                       )
                                 )

    status = forms.ModelChoiceField(queryset=Status.objects.all(),
                                    label='Статус вакансии',
                                    widget=forms.Select(attrs={
                                        'class':'form-control',
                                        'placeholder':'Выберите статус'
                                    })
                                    )

    class Meta:
        model = Vacancy
        fields = ("salary","end_date","description")
        labels = {
            #'position': _(u'Должность'),
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


        }




