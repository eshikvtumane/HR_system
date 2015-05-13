#-*- coding: utf8 -*-
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.forms import ModelForm
from events.models import ApplicantVacancyEvent, Event
from vacancies.models import Vacancy,Department,VacancyStatus,Head
from applicants.models import Position

class VacancyForm(ModelForm):
     class Meta:
        model = Vacancy
        labels = {
            'salary': _(u'Зарплата'),
            'end_date': _(u'Предполагамый срок закрытия'),
            'additional_info': _(u'Дополнительная информация'),

        }
        widgets = {
            'salary': forms.NumberInput(attrs={
                'class': "form-control",
                'name':'salary',
                'min': 0,
                'data-validation': 'number',
                'data-validation-allowing': 'float',
                'data-validation-error-msg':"В поле зарплаты должно быть указано число!"
            }),
            'end_date': forms.DateInput(attrs={
                'id':'end_date',
                'class': "form-control",
                'name':'end_date',
                'data-validation': "date",
                'data-validation-format': "dd-mm-yyyy",
                'data-validation-error-msg':"Вы ввели некорректную дату!"

            }),

            'position':forms.Select(attrs={
                'class':'select',
                'id':'position',
                'data-validation':'required',
                'data-validation-error-msg':"Это поле обязательно для заполнения!"
            }),

            'sex':forms.Select(attrs={
                'class':'select',
                'id':'sex',

            }),

            'marriage_status':forms.Select(attrs={
                'class':'select',
                'id':'marriage_status',

            }),

             'paid_vacation':forms.NumberInput(attrs={
                'class':'form-control',
                'id':'paid_vacation',
                'min': 0
            }),
            'duties':forms.Textarea(attrs={
                'class':'form-control',
                'id':'duties',

            }),

             'creation_reason':forms.Textarea(attrs={
                'class':'form-control',
                'id':'creation_reason',

            }),

            'further_education':forms.Textarea(attrs={
                'class':'form-control',
                'id':'further_education',

            }),

            'skills':forms.Textarea(attrs={
                'class':'form-control',
                'id':'skills',

            }),
        }


class AddVacancyForm(VacancyForm):

    class Meta(VacancyForm.Meta):
        exclude = ['published_at']



class EditVacancyForm(VacancyForm):
   status = forms.ModelChoiceField(queryset=VacancyStatus.objects.all(),
                                   label='Статус',
                                   widget=forms.Select(attrs={
                                     'class':'select' })

         )


   class Meta(VacancyForm.Meta):
       exclude = ['position','author','head','last_status','published_at']

class SearchVacancyForm(VacancyForm):

    status = forms.ModelChoiceField(queryset=VacancyStatus.objects.all(),
                                   label=_(u'Статус'),
                                   widget=forms.Select(attrs={
                                     'class':'select' })

                                   )

    head = forms.ModelChoiceField(queryset=Head.objects.all(),
                                   label=_(u'Руководитель'),
                                   widget=forms.Select(attrs={
                                     'class':'select' })

                                   )


    search_start = forms.DateField(label=_(u'Начальная дата поиска'),widget=forms.DateInput(attrs={
        'class':'form-control'
    }))

    search_end = forms.DateField(label=_(u'Конечная дата поиска'),widget=forms.DateInput(attrs={
        'class':'form-control'
    }))


class ApplicantVacancyEventForm(ModelForm):
    class Meta:
        model=ApplicantVacancyEvent
        fields = { 'event' ,'start','end',}

    widgets={

        'event': forms.Select(attrs={'class':'select','id':'event'}),

        'start': forms.DateTimeInput(attrs={
            'id': 'start',
            'class': 'form-control',
            'name': 'start'
        }),
        'end': forms.DateTimeInput(attrs={
            'id': 'end',
            'class': 'form-control',
            'name': 'end'
        })
    }