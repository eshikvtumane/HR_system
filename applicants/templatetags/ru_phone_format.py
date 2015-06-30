#-*- encoding: utf-8 -*-
from django import template

register = template.Library()

@register.filter(name='phone_format')
def phone_format(value):
    value = str(value)
    phone_len = len(value)

    code_khv = '4212'

    if phone_len == 4:
        return '(гор) - (%s) %s %s‒%s' % (code_khv, value[:2],value[2:])
    if phone_len == 5:
        return '(гор) - (%s) %s‒%s‒%s' % (code_khv, value[:1],value[1:3], value[3:])
    if phone_len == 6:
        return '(гор) - (%s) %s‒%s‒%s' % (code_khv, value[:2], value[2:4], value[4:])
    if phone_len == 7:
        return '(гор) - (%s) %s‒%s‒%s' % (code_khv, value[:3], value[3:5], value[5:])
    if phone_len == 10:
        return '(сот) -  8 %s %s‒%s‒%s' % (value[:3], value[3:6], value[6:8], value[8:])
    if phone_len == 11:
        return '(сот) -  8 %s %s‒%s‒%s' % (value[1:4], value[4:7], value[7:9], value[9:])

    return value

    #if phone_len == 11:
        #return '+7 (%s) %s‒%s‒%s' % (value[:3], value[3:5], value[5:])

