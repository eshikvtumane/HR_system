#-*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url
from views import EmailConstructorView, SavingImageAjax, SavingTinyMCEImage, SavingTemplatesAjax, LoadTemplateAjax, GenerateThumbnail, EmailSender

urlpatterns = patterns('',
    url(r'^$', EmailConstructorView.as_view(), name='create_email'),

    # сохранение загруженного изображения на сервере
    url(r'^save_img/$', SavingImageAjax.as_view(), name='save_img'),
    url(r'^save_tinymce_img/$', SavingTinyMCEImage.as_view(), name='save_tinymce_img'),

    # сохранение шаблона
    url(r'^save_template/$', SavingTemplatesAjax.as_view(), name='save_template'),

    # загрузка выбранного шаблона
    url(r'^load_template/$', LoadTemplateAjax.as_view(), name='load_template'),

    # генерирование эскиза для видео
    url(r'^generate_thumbnail/$', GenerateThumbnail.as_view(), name='generate_thumbnail'),

    # рассылка письма
    url(r'^email_sender/$', EmailSender.as_view(), name='email_sender'),
)