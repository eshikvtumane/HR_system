#-*- encoding: utf-8 -*-
from django import template
from applicants.forms import VacancyForm
from datetime import datetime, date

register = template.Library()

@register.filter(name='global_vacancy_form')
@register.inclusion_tag('/applicants/includes/vacancy.html', takes_context=True)
def global_vacancy_form():
    print 'FILTER'
    return dict(formVacancy=VacancyForm(), t='AAAAAAAAAAAA')


from django.contrib.auth.forms import AuthenticationForm

register = template.Library()

@register.inclusion_tag('_tag_auth_form.html')
def authentication_form():
    return {'form': AuthenticationForm(), 'action': '/some/url'}


