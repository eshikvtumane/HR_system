#-*- coding: utf8 -*-
from django import forms
from models import Applicant, ApplicantEducation, Education, Major, Position, SourceInformation
from vacancies.models import Vacancy

from datetime import datetime

# Create your forms here.
class ApplicantForm(forms.ModelForm):
    """
        Форма для добавления кандидата в базу
    """

    class Meta:
        model = Applicant
        fields = '__all__'
        exclude = ('date_created',)
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': "form-control",
                'data-validation': "custom", 'data-validation-regexp': "^([А-Яа-яЁё -]+)$",
                'data-validation-error-msg': "Фамилия должна состоять из кириллических символов",
                'autocomplete': 'off'
            }),
            'last_name': forms.TextInput(attrs={
                'class': "form-control",
                'data-validation': "custom",
                'data-validation-regexp': "^([А-Яа-яЁё]+)$",
                'data-validation-error-msg': "Имя должно состоять из кириллических символов",
                'autocomplete': 'off'
            }),
            'middle_name': forms.TextInput(attrs={
                 'class': "form-control",
                 'data-validation': "middle_name",
                'autocomplete': 'off'
            }),
            'sex': forms.Select(attrs={
                'class': 'select',
                'placeholder': 'Выберите пол'
            }),
            'birthday': forms.DateInput(attrs={
                'class': "form-control",
                'data-validation': "date",
                'data-validation-format': "dd-mm-yyyy"
            }),
            'photo': forms.FileInput(attrs={'accept':'image/*',
                                            'class': 'upload'
                                            }),
            'city': forms.TextInput(attrs={
                'class': "form-control",
                #'data-validation': "text",
                'autocomplete': 'off'
            }),
            'street': forms.TextInput(attrs={
                'class': "form-control",
                #'data-validation': "text",
                'autocomplete': 'off'
            }),

            'building': forms.TextInput(attrs={
                'class': "form-control",
                'autocomplete': 'off'
                #'data-validation': "custom",
                #'data-validation-regexp': "^([А-Яа-яЁё]+)$",
                #'data-validation-error-msg': "Название города должно состоять из кириллических символов"
            }),
            'email': forms.EmailInput(attrs={
                'class': "form-control",
                'data-validation': "address",
                'autocomplete': 'off'
            }),
            'skype': forms.TextInput(attrs={
                'class': "form-control",
                'data-validation': "skype",
                'autocomplete': 'off'
            }),
            'icq': forms.TextInput(attrs={
                'class': "form-control",
                'data-validation': "icq",
                'autocomplete': 'off'
            }),
            'vk': forms.TextInput(attrs={
                'class': "form-control",
                'autocomplete': 'off'
            }),
            'fb': forms.TextInput(attrs={
                'class': "form-control",
                'autocomplete': 'off'
            }),
            'note': forms.Textarea(attrs={
                'class': "form-control",
                'rows': '3',
                'cols': '3',
                'autocomplete': 'off'
            })
        }

# кортеж годов (для выбора начала обучения)
YEAR = tuple(
        (str(i), i)
        for i in xrange(datetime.now().year, 1901, -1)
    )

# Форма добавления образования
class ApplicantEducationForm(forms.ModelForm):
    education = forms.ModelChoiceField(queryset=Education.objects.all(),
                                       label='Образование',
                                       widget=forms.Select(attrs={
                                           'class':'select',
                                            'placeholder':'Выберите образование'
                                       })
            )

    major = forms.ModelChoiceField(queryset=Major.objects.all(),
                                            label='Специальность',
                                            widget=forms.Select(attrs={
                                                'class': 'select-add',
                                                'placeholder':'Выберите специальность'
                                                }
                                            )
            )

    class Meta:
        model = ApplicantEducation
        fields = ('education', 'major', 'study_start', 'study_end')
        widgets = {
            'study_start': forms.Select(choices=YEAR,
                                        attrs={
                                                'class': 'select',
                                                'placeholder':'Выберите год'
                                            }
            ),
            'study_end': forms.NumberInput(attrs={
                                                'class': 'form-control'
                                            })
        }

# Форма выбора вакансий
class VacancyAddForm(forms.Form):
    position = forms.ModelChoiceField(queryset=Position.objects.all(),
                                       label='Должность',
                                       widget=forms.Select(attrs={
                                           'class':'select',
                                            'placeholder':'Выберите должность'
                                       })
            )
    '''vacancies = forms.ModelChoiceField(label='Вакансии',
                                       widget=forms.Select(attrs={
                                           'class':'select',
                                            'placeholder':'Выберите вакансию'
                                       })
            )'''

# Форма поиска
class CandidateSearchForm(forms.Form):
    GENDER_LIST = (
        ('', 'Выберите пол'),
        ('1', 'Мужской'),
        ('2', 'Женский'),
    )

    # фамилия
    first_name = forms.CharField(label='Фамилия',
                                 widget=forms.TextInput(attrs={
                                     'class': 'form-control'
                                 })
                                )
    # имя
    last_name = forms.CharField(label='Имя',
                                 widget=forms.TextInput(attrs={
                                     'class': 'form-control'
                                 })
    )
    # отчество
    middle_name = forms.CharField(label='Отчество',
                                 widget=forms.TextInput(attrs={
                                     'class': 'form-control'
                                 })
    )
    # почта
    email = forms.EmailField(widget=forms.EmailInput(attrs={
                                         'class':'form-control',
                                     }))
    # пол
    sex = forms.ChoiceField(choices=GENDER_LIST,
                                 widget=forms.Select(attrs={
                                     'class': 'select',
                                     'data-placeholder': 'Выберите пол'
                                 })
                                 )
    # Место жительства
    city = forms.ChoiceField(
                                 widget=forms.Select(attrs={
                                     'class': 'select',
                                     'placeholder': 'Выберите город'
                                 })
                                 )
    # должность
    position =forms.ModelChoiceField(queryset=Position.objects.all(),
                                     label='Должность',
                                     widget=forms.Select(attrs={
                                         'class': 'select',
                                         'placeholder': 'Выберите должность'
                                     }
                                )
                            )

    # включить возраст в поиск
    age_add = forms.BooleanField(widget=forms.CheckboxInput(attrs={
                                       })
            )
    age_start = forms.Field(widget=forms.HiddenInput())
    age_end = forms.Field(widget=forms.HiddenInput())

    # включить зарплату в поиск
    salary_add = forms.BooleanField(widget=forms.CheckboxInput(attrs={
                                       })
            )
    salary_start = forms.Field(widget=forms.HiddenInput())
    salary_end = forms.Field(widget=forms.HiddenInput())

    reserve = forms.BooleanField(label='Резерв',
                                       widget=forms.CheckboxInput(attrs={
                                       })
            )

    employee = forms.BooleanField(widget=forms.CheckboxInput(attrs={
                                       })
            )

class VacancyForm(forms.Form):

    position = forms.ModelChoiceField(queryset=Position.objects.all(),
                                     widget=forms.Select(attrs={
                                         'placeholder': 'Выберите должность',
                                         'class':'select',
                                         'id': 'position',
                                         'name': 'position'
                                     }
                                    )
    )

    vacancy = forms.ModelChoiceField(queryset=[],
                                     widget=forms.Select(attrs={
                                         'placeholder': 'Выберите вакансию',
                                         'class': 'select',
                                         'id': 'vacancies',
                                         'name': 'vacancies'
                                     }
                                    )
    )
    '''
    salary = forms.IntegerField(widget=forms.NumberInput(attrs={
                                        'id': 'salary',
                                         'name': 'salary'
                                }))
    suggested_salary = forms.NumberInput(widget=forms.NumberInput(attrs={
                                        'id': 'suggested_salary',
                                         'name': 'suggested_salary'
                                }))'''
    source = forms.ModelChoiceField(queryset=SourceInformation.objects.all(),
                                       label='Источник',
                                       widget=forms.Select(attrs={
                                           'class':'select-add',
                                            'placeholder':'Выберите источник',
                                            'id': 'source[]',
                                            'name': 'source[]'
                                       })
    )