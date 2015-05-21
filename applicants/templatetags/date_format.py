#-*- encoding: utf-8 -*-
from django import template
from datetime import datetime, date

register = template.Library()

@register.filter(name='date_format')
def date_format(value):
    value = str(value).split(' ')
    return value[0]


@register.filter(name='age')
def age(born):
    if born:
        year_words = [
            u'год',
            u'года',
            u'лет'
        ]
        today = date.today()
        age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        return str(age) + ' ' + __getDeclension(age, year_words)
    return ''

@register.filter(name='applicant_declention')
def applicant_declention(number):
    applicant_words = [
            u'кандидат',
            u'кандидата',
            u'кандидатов'
        ]
    return __getDeclension(number, applicant_words) + u' в базе'

@register.filter(name='number_declention')
def number_declention(number):
    year_words = [
            u'год',
            u'года',
            u'лет'
        ]
    return __getDeclension(number, year_words)

def __getDeclension(number, year_words):
    string_list = []
    if number != 0 and isinstance(number, int):
        number = str(number)
        number_len = len(number)
        int_number = int(number[number_len-1])
        if int(number) > 10 and int(number) < 20:
            string_list.append(year_words[2])
        elif int_number == 1:
            string_list.append(year_words[0])
        elif int_number > 1 and int_number < 5:
            string_list.append(year_words[1])
        else:
            string_list.append(year_words[2])
    return u' '.join(string_list)


