#-*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url
from views import SummaryStatementRecruitment, MainReports, SummaryStatementRecruitmentGenerateAjax, PositionStatement

urlpatterns = patterns('',

    url(r'^$', MainReports.as_view(), name='main_reports'),

    # генерирование сводной ведомость по наботу персонала
    url(r'^summary_statement/$', SummaryStatementRecruitment.as_view(), name='statement_recruitment_report'),
    url(r'^summary_statement_generate/$', SummaryStatementRecruitmentGenerateAjax.as_view(), name='statement_recruitment_report_generate'),

    # генерирование ведомости с информацией о персонале за определённый год
    url(r'^employers_info/$', PositionStatement.as_view(), name='employers_info_report'),
)