#-*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url
from views import EmailConstructorView, SavingImageAjax

urlpatterns = patterns('',
    url(r'^create/$', EmailConstructorView.as_view(), name='create_email'),

    # сохранение загруженного изображения на сервере
    url(r'^save_img/$', SavingImageAjax.as_view(), name='save_img'),
)