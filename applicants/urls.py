#-*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url
from views import ApplicantAddView, ApplicantSearchView, VacancySearchAjax, \
    ApplicantView, ApplicantVacancyStatusAjax, PositionSourceGetAjax, PhotoDeleteAjax, PhoneDeleteAjax

urlpatterns = patterns('',

    # добавление нового кандидата в базу
    url(r'^add/$', ApplicantAddView.as_view(), name='applicant_add'),
    # поиск кандидатов
    url(r'^search/$', ApplicantSearchView.as_view(), name='applicant_search'),
    # страница кандидата
    url(r'^view/(?P<applicant_id>[0-9]+)/$', ApplicantView.as_view(), name='applicant_view'),
    # выборка вакансий
    url(r'^vacancy_search/$', VacancySearchAjax.as_view(), name='vacancy_search'),
    # добавление статуса кандидату
    url(r'^status_add/$', ApplicantVacancyStatusAjax.as_view()),

    # получение должностей и источников
    url(r'^position_source_get/$', PositionSourceGetAjax.as_view()),

    # удаление фото со страницы кандидата
    url(r'^delete_photo/$', PhotoDeleteAjax.as_view()),

    # удаление номера телефона со страницы кандидата
    url(r'^delete_phone/$', PhoneDeleteAjax.as_view()),

    #url(r'^admin/', include(admin.site.urls)),
)