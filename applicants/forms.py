#-*- coding: utf8 -*-
from django import forms
from models import Applicant, ApplicantEducation, Education, Major

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




    class Meta:
        model = Applicant
        fields = ( 'first_name', 'last_name', 'middle_name', 'birthday', 'photo', 'experience', 'phone', 'email', 'icq', 'skype', )
        widgets = {
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'middle_name': forms.TextInput(),
            'birthday': forms.DateInput(format='%d-%m-%Y', attrs={'class':''}),
            'photo': forms.FileInput(attrs={'accept':'.jpg, .jpeg, .png, .gif'})
        }

class ApplicantEducationForm(forms.ModelForm):

    education = forms.ModelChoiceField(queryset=Education.objects.all(), label='Образование', widget=forms.Select(attrs={'class':'select-color'}))
    major = forms.ModelChoiceField(queryset=Major.objects.all(), label='Специальность', widget=forms.Select(attrs={'class':'select-color'}))


    class Meta:
        model = ApplicantEducation
        fields = ( 'education', 'major' )

