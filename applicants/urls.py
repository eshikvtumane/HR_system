#-*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url
from views import ApplicantAddView, CandidateSearchView, VacancySearchAjax, \
    ApplicantView, ApplicantVacancyStatusAjax,ApplicantEventAjax

urlpatterns = patterns('',

    # добавление нового кандидата в базу
    url(r'^add/$', ApplicantAddView.as_view(), name='applicant_add'),
    # поиск кандидатов
    url(r'^search/$', CandidateSearchView.as_view(), name='applicant_search'),
    # страница кандидата
    url(r'^view/(?P<applicant_id>[0-9]+)/$', ApplicantView.as_view(), name='applicant_view'),
     url(r'^view/(?P<applicant_id>[0-9]+)/add_event/$',
         ApplicantEventAjax.as_view(), name='applicant_event'),

    # выборка вакансий
    url(r'^vacancy_search/$', VacancySearchAjax.as_view(), name='vacancy_search'),
    # добавление статуса кандидату
    url(r'^status_add/$', ApplicantVacancyStatusAjax.as_view()),

    #url(r'^admin/', include(admin.site.urls)),
)