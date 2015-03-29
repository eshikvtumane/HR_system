#-*- coding: utf8 -*-
from django import forms
from applicants.models import Position, SourceInformation

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