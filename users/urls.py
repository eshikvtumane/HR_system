#-*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url
from views import LoginView, LogoutView, PasswordChangeView, PasswordResetView

urlpatterns = patterns('',


    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),

    url(r'^change_password/$', PasswordChangeView.as_view(), name='change_password'),
    url(r'^reset_password/$', PasswordResetView.as_view(), name='reset_password'),
)