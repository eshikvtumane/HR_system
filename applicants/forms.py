#-*- coding: utf8 -*-
from django import forms
from models import Applicant, ApplicantEducation, Education, Major, Position, SourceInformation

# Create your forms here.
class ApplicantForm(forms.ModelForm):
    """
        Форма для добавления кандидата в базу
    """
    '''first_name = forms.CharField(widget=forms.TextInput)
    last_name = forms.CharField(widget=forms.TextInput)
    middle_name = forms.CharField(widget=forms.TextInput)

    # Дата рождения
    birthday = forms.DateField(widget=forms.DateField)

    # Фотография кандидата
    photo = forms.FileField(widget=forms.FileField)
'''
    source = forms.ModelChoiceField(queryset=SourceInformation.objects.all(),
                                       label='Источник',
                                       widget=forms.Select(attrs={
                                           'class':'',
                                            'placeholder':'Выберите источник'
                                       })
            )

    class Meta:
        model = Applicant
        exclude = ('id',)
        #fields = ( 'first_name', 'last_name', 'middle_name', 'birthday', 'photo', 'phone', 'email', 'icq', 'skype', 'city', 'street', 'building')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': "form-control",
                'data-validation': "custom", 'data-validation-regexp': "^([А-Яа-яЁё]+)$",
                'data-validation-error-msg': "Фамилия должна состоять из кириллических символов"
            }),
            'last_name': forms.TextInput(attrs={
                'class': "form-control",
                'data-validation': "custom",
                'data-validation-regexp': "^([А-Яа-яЁё]+)$",
                'data-validation-error-msg': "Имя должно состоять из кириллических символов"
            }),
            'middle_name': forms.TextInput(attrs={
                 'class': "form-control",
                 'data-validation': "middle_name"
            }),
            'birthday': forms.DateInput(attrs={
                'class': "form-control",
                'data-validation': "date",
                'data-validation-format': "dd-mm-yyyy"
            }),
            'photo': forms.FileInput(attrs={'accept':'.jpg, .jpeg, .png, .gif, .bmp'}),
            'city': forms.TextInput(attrs={
                'class': "form-control",
                'data-validation': "custom",
                'data-validation-regexp': "^([А-Яа-яЁё]+)$",
                'data-validation-error-msg': "Название города должно состоять из кириллических символов"
            }),
            'street': forms.TextInput(attrs={
                'class': "form-control",
                'data-validation': "custom",
                'data-validation-regexp': "^([А-Яа-яЁё]+)$",
                'data-validation-error-msg': "Название улицы должно состоять из кириллических символов"
            }),

            'building': forms.TextInput(attrs={
                'class': "form-control"
                #'data-validation': "custom",
                #'data-validation-regexp': "^([А-Яа-яЁё]+)$",
                #'data-validation-error-msg': "Название города должно состоять из кириллических символов"
            }),
            'phone': forms.TextInput(attrs={
                'class': "form-control",
                'data-validation': "number"
            }),
            'email': forms.EmailInput(attrs={
                'class': "form-control",
                'data-validation': "email"
            }),
            'skype': forms.TextInput(attrs={
                'class': "form-control",
                'data-validation': "skype"
            }),
            'icq': forms.TextInput(attrs={
                'class': "form-control",
                'data-validation': "icq"
            }),
            'vk': forms.TextInput(attrs={
                'class': "form-control"
            }),
            'fb': forms.TextInput(attrs={
                'class': "form-control"
            })
        }

# Форма добавления оюрахования
'''class ApplicantEducationForm(forms.ModelForm):
    class Meta:
        model = ApplicantEducation
        fields = ( 'education', 'major' )
        widgets = {
            'education': forms.ModelChoiceField(queryset=Education.objects.all(),
                                       label='Образование',
                                       widget=forms.Select(attrs={
                                           'class':'select-color',
                                            'placeholder':'Выберите образование'
                                       })
            ),
            'major': forms.ModelChoiceField(queryset=Major.objects.all(),
                                            label='Специальность',
                                            widget=forms.Select(attrs={
                                                'placeholder':'Выберите специальность'
                                                }
                                            )
            ),
            'study_start': forms.NumberInput(),
            'study_end': forms.NumberInput()
        }'''

# Форма поиска
class CandidateSearchForm(forms.Form):
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
    email = forms.EmailField(widget=forms.EmailInput())
    # опыт работы
    experience = forms.CharField(label='Опыт работы',
                                 widget=forms.TextInput(attrs={
                                     'class': 'form-control'
                                 })
                                 )

    # должность
    position =forms.ModelChoiceField(queryset=Position.objects.all(),
                                     label='Должность',
                                     widget=forms.Select(attrs={
                                         'placeholder': 'Выберите должность'
                                     }
                                )
                            )

    salary = forms.IntegerField(label='Запрашиваемая зарплата',
                                widget=forms.NumberInput(attrs={
                                     'class': 'form-control'
                                 })
                                )





