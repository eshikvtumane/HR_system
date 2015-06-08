#-*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url
from views import EventsView,EventsAdd,EventsCalendar
from django.contrib.admin.views.decorators import staff_member_required

urlpatterns = patterns('',

     url(r'^(?P<applicant_id>[0-9]+)/$', staff_member_required(EventsView.as_view()), name='events_view'),

     url(r'^(?P<applicant_id>[0-9]+)/add_event/$',staff_member_required(EventsAdd.as_view()), name='add_event'),

    url(r'^events_calendar/$',staff_member_required(EventsCalendar.as_view()),name='events_calendar'),

     url(r'^get_events/$','events.views.get_events_ajax'),

     url(r'^get_vacancy_events/$', 'events.views.get_vacancy_events_ajax', name='get_vacancy_events'),

     url(r'^add_event$','events.views.add_event', name='add_event'),

     url(r'^add_event_comment$', 'events.views.add_event_comment_ajax'),

     url(r'^update_event/$','events.views.update_event_ajax'),

     url(r'^delete_event/$','events.views.delete_event_ajax'),

     url(r'^send_message/$','events.views.send_message_ajax')

)