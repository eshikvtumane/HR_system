#-*- encoding: utf-8 -*-
from django import template

register = template.Library()

@register.filter(name='date_format')
def date_format(value):
    value = str(value).split(' ')
    print 'Date'
    print value, len(value)
    return value[0]
    '''
    month = {
        'января': '01',
        'февраля': '02',
        'марта': '03',
        'апреля': '04',
        'мая': '05',
        'июня': '06',
        'июля': '07',
        'августа': '08',
        'сентября': '09',
        'октября': '10',
        'ноября': '11',
        'декабря': '12'
    }
    # day
    day = value[0]
    if len(day) != 2:
        day = '0' + day
    # month
    m = month[value[1]]
    # year
    y = value[2]

    return '%s-%s-%s' % (day, m, y)
'''
