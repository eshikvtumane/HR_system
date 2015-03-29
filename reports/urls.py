#-*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url
from views import SummaryStatementRecruitment, MainReports

urlpatterns = patterns('',
    # генерирование сводной ведомость по наботу персонала
    url(r'^$', MainReports.as_view(), name='main_reports'),
    url(r'^summary_statement/$', SummaryStatementRecruitment.as_view(), name='statement_recruitment_report'),
)