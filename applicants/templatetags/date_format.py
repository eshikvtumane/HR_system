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
    today = date.today()
    print born
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))