#-*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url
from views import EventsView,EventsAdd

urlpatterns = patterns('',

     url(r'^(?P<applicant_id>[0-9]+)/$', EventsView.as_view(), name='events_view'),

     url(r'^(?P<applicant_id>[0-9]+)/add_event/$',EventsAdd.as_view(), name='add_event'),

     url(r'^get_events/$','events.views.get_events_ajax'),

     url(r'^get_vacancy_events/$', 'events.views.get_vacancy_events_ajax', name='get_vacancy_events'),

     url(r'^add_event$','events.views.add_event', name='add_event'),

     url(r'^change_event_status$', 'events.views.change_event_status_ajax', name='change_event_status'),

     url(r'^update_event/$','events.views.update_event_ajax'),

     url(r'^delete_event/$','events.views.delete_event_ajax')

)