#-*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url
from views import ApplicantAddView, CandidateSearchView, ApplicantView, VacancySearchAjax


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'HR_project.vSiews.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # добавление нового кандидата в базу
    url(r'^add/$', ApplicantAddView.as_view(), name='applicant_add'),
    # поиск кандидатов
    url(r'^search/$', CandidateSearchView.as_view(), name='applicant_search'),
    # страница кандидата
    url(r'^view/?P<applicant_id>[0-9]+/$', ApplicantView.as_view(), name='applicant_view'),

    # выборка вакансий
    url(r'^vacancy_search/$', VacancySearchAjax.as_view(), name='vacancy_search'),



    #url(r'^admin/', include(admin.site.urls)),
)