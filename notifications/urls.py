from django.conf.urls import patterns, include, url
from django.contrib import admin
from .views import Notifications

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', Notifications.as_view(), name='notifications_view'),

)

