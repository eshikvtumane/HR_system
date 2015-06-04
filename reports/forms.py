#-*- coding: utf8 -*-
from django import forms
from applicants.models import Position, SourceInformation
from datetime import datetime

# Create your forms here.
class SummaryStatementRecruimentForm(forms.Form):
    period = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'date-picker',
        'id': 'period'
    }))
    position = forms.ModelChoiceField(queryset=Position.objects.all(),
                                     widget=forms.Select(attrs={
                                         'placeholder': 'Выберите должность',
                                         'class':'select',
                                         'id': 'position',
                                         'name': 'position',
                                          'data-placeholder': "Выберите должность..."
                                     }
                                    )
    )

    vacancies = forms.ChoiceField(widget=forms.Select(attrs={
                                     'class': 'select-vacancy',
                                     'placeholder': 'Выберите вакансию',
                                     'id': 'vacancies'
                                 })
    )

    source = forms.ModelChoiceField(queryset=SourceInformation.objects.all(),
                                       label='Источник',
                                       widget=forms.Select(attrs={
                                           'class':'select-source',
                                           'placeholder': 'Выберите источники',
                                           'multiple': 'multiple',
                                            'id': 'source',
                                            'name': 'source'
                                       })
    )

YEAR = tuple(
        (str(i), i)
        for i in xrange(datetime.now().year, 2000, -1)
    )

class PositionStatementForm(forms.Form):
    position = forms.ModelChoiceField(queryset=Position.objects.all(),
                                     widget=forms.Select(attrs={
                                         'placeholder': 'Выберите должность',
                                         'class':'select',
                                         'id': 'position',
                                         'name': 'position',
                                          'data-placeholder': "Выберите должность..."
                                     }
                                    )
    )

    year = forms.ChoiceField(choices=YEAR,
                                 widget=forms.Select(attrs={
                                     'class': 'select',
                                     'data-placeholder': 'Выберите год'
                                 })
                                 )