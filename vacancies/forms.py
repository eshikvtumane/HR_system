#-*- coding: utf8 -*-
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.forms import ModelForm
from events.models import ApplicantVacancyEvent, Event
from vacancies.models import Vacancy,Department,VacancyStatus,Head
from applicants.models import Position


class AddVacancyForm(ModelForm):

    class Meta:
        model = Vacancy
        exclude = ['published_at']
        labels = {
            'salary': _(u'Зарплата'),
            'end_date': _(u'Предполагамый срок закрытия'),
            'additional_info': _(u'Дополнительная информация'),

        }
        widgets = {
            'salary': forms.NumberInput(attrs={
                'class': "form-control",
                'name':'salary',
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
                'class':'form-control',
                'id':'position',
                'data-validation':'required',
                'data-validation-error-msg':"Это поле обязательно для заполнения!"
            }),

            'sex':forms.Select(attrs={
                'class':'form-control',
                'id':'sex',

            }),

            'marriage_status':forms.Select(attrs={
                'class':'form-control',
                'id':'marriage_status',

            }),

             'paid_vacation':forms.NumberInput(attrs={
                'class':'form-control',
                'id':'paid_vacation',

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



class EditVacancyForm(ModelForm):
   status = forms.ModelChoiceField(queryset=VacancyStatus.objects.all(),
                                   label='Статус',
                                   widget=forms.Select(attrs={
                                     'class':'select' })

         )
   class Meta:
        model = Vacancy
        fields = ("salary","end_date","additional_info")
        labels = {
            'salary': _(u'Зарплата'),
            'end_date': _(u'Предполагамый срок закрытия'),
            'additional_info': _(u'Описание'),

        }
        widgets = {
            'salary': forms.NumberInput(attrs={
                'class': "form-control",
                'name':'salary',
                'data-validation': 'number',
                'data-validation-allowing': 'float',
                'data-validation-error-msg':"В поле зарплаты должно быть указано число!"

            }),
            'end_date': forms.DateInput(format=('%d-%m-%Y'),attrs={
                'id':'end_date',
                'class': "form-control",
                'name':'end_date',
                'data-validation': "date",
                'data-validation-format': "dd-mm-yyyy",
                'data-validation-error-msg':"Вы ввели некорректную дату!"

            }),
            'additional_info':forms.Textarea(attrs={
                'class':'form-control'


            })



        }


class SearchVacancyForm(ModelForm):

    status = forms.ModelChoiceField(queryset=VacancyStatus.objects.all(),
                                   label=_(u'Статус'),
                                   widget=forms.Select(attrs={
                                     'class':'form-control' })

                                   )

    head = forms.ModelChoiceField(queryset=Head.objects.all(),
                                   label=_(u'Руководитель'),
                                   widget=forms.Select(attrs={
                                     'class':'form-control' })

                                   )


    search_start = forms.DateField(label=_(u'Начальная дата поиска'),widget=forms.DateInput(attrs={
        'class':'form-control'
    }))

    search_end = forms.DateField(label=_(u'Конечная дата поиска'),widget=forms.DateInput(attrs={
        'class':'form-control'
    }))

    class Meta:
        model = Vacancy
        fields = ("salary","end_date","additional_info",'head','position')
        labels = {
            'salary': _(u'Зарплата'),
            'end_date': _(u'Предполагамый срок закрытия'),
            'additional_info': _(u'Описание'),

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
            'additional_info':forms.Textarea(attrs={
                'class':'form-control'

            }),
            'position':forms.Select(attrs={'class':'form-control','id':'position'})
        }



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