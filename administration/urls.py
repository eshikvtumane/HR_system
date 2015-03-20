#-*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url
from views import ValueAddView, MajorSaveView, SourceSaveView, VacancyStatusSaveView


urlpatterns = patterns('',
    url(r'^add/$', ValueAddView.as_view(), name='add'),


    # добавление специальностей из списка через ajax
    url(r'^ajax_source_add/$', SourceSaveView.as_view()),
    # добавление специальностей через ajax
    url(r'^ajax_spec/$', MajorSaveView.as_view()),
    # добавление статусов вакансий через ajax
    url(r'^ajax_vacancy/$', VacancyStatusSaveView.as_view()),

)