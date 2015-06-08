from django.conf.urls import patterns,url
from views import *

from django.contrib.admin.views.decorators import staff_member_required


urlpatterns = patterns('',
    url(r'^add/$',staff_member_required(AddVacancy.as_view()),name='vacancy_add'),
    url(r'^(?P<id>[0-9]+)/$',staff_member_required(VacancyView.as_view()),name='vacancy_view'),
    url(r'^(?P<id>[0-9]+)/edit/$',staff_member_required(VacancyEdit.as_view()),name='vacancy_edit'),
    url(r'^search/$',staff_member_required(VacancySearch.as_view()),name='vacancy_search'),
    #ajax handlers
    url(r'^get_heads/$','vacancies.views.get_heads_ajax'),

    #url(r'^add/$', .as_view()),
    #url(r'^admin/', include(admin.site.urls)),
)