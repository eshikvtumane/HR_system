from django.conf.urls import patterns,url
from views import *


urlpatterns = patterns('',
    url(r'^add/$',AddVacancy.as_view(),name='vacancy_add'),
    url(r'^(?P<id>[0-9]+)/$',VacancyView.as_view(),name='vacancy_view'),
    url(r'^(?P<id>[0-9]+)/edit/$',VacancyEdit.as_view(),name='vacancy_edit'),
    url(r'^search/$',VacancySearch.as_view(),name='vacancy_search'),
    #ajax handlers
    url(r'^get_heads/$','vacancies.views.get_heads_ajax'),

    #url(r'^add/$', .as_view()),
    #url(r'^admin/', include(admin.site.urls)),
)