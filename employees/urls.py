#-*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url
from views import EmployeesView

urlpatterns = patterns('',

    #
    url(r'^add/$', EmployeesView.as_view(), name='employees_view'),

)