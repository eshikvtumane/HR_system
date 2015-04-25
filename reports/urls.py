#-*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url
from views import SummaryStatementRecruitment, MainReports, SummaryStatementRecruitmentGenerateAjax, PositionStatement, VacancyReport, VacancyReportGenerateAjax

urlpatterns = patterns('',

    url(r'^$', MainReports.as_view(), name='main_reports'),

    # генерирование сводной ведомость по наботу персонала
    url(r'^summary_statement/$', SummaryStatementRecruitment.as_view(), name='statement_recruitment_report'),
    url(r'^summary_statement_generate/$', SummaryStatementRecruitmentGenerateAjax.as_view(), name='statement_recruitment_report_generate'),

    # генерирование ведомости с информацией о персонале за определённый год
    url(r'^employers_info/$', PositionStatement.as_view(), name='employers_info_report'),

    # генерирование ведомости с информацией о вакансиях
    url(r'^vacancy_report_generate/$', VacancyReport.as_view(), name='vacancy_report'),
    url(r'^vacancy_report_generate_ajax/$', VacancyReportGenerateAjax.as_view(), name='vacancy_report_ajax'),
)