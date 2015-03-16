#-*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url
from views import ApplicantAddView, CandidateSearchView, VacancySearchAjax


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'HR_project.vSiews.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # добавление нового кандидата в базу
    url(r'^add/$', ApplicantAddView.as_view(), name='applicant_add'),
    # поиск кандидатов
    url(r'^search/$', CandidateSearchView.as_view(), name='applicant_search'),

    # выборка вакансий
    url(r'^vacancy_search/$', VacancySearchAjax.as_view(), name='vacancy_search'),

    #url(r'^admin/', include(admin.site.urls)),
)