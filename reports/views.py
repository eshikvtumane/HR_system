#-*- coding: utf8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import View

from forms import SummaryStatementRecruimentForm
import json
import xlwt

# Create your views here.
class MainReports(View):
    template = 'reports/reports.html'
    def get(self, request):
        return render_to_response(self.template, RequestContext(request))


class GenerateReport():
    def __init__(self):
        self.wb = xlwt.Workbook(encoding='utf-8')

    def createWorksheet(self, sheet_name):
        ws = self.wb.add_sheet(sheet_name)

    def writeHead(self, ws, values, row_start, column_start=0):
        for value in values:
            if isinstance(value[0], dict):
                print 'dict'
                self.writeHead(ws, value[value.keys()[0]], row_start+1, column_start)
                self.writeValues(value[0])
            else:
                ws.write(row_start, column_start, value[0])

            column_start += 1
        return

    def __writeDictionary(self, dictionary):
        for key in dictionary.keys():
            if isinstance(dictionary[key], dict):
                pass

    def saveWorkbook(self, name='report'):
        self.wb.save(name)
        return True


# Сводная ведомость по набору персонала
class SummaryStatementRecruitment(View):
    template = 'reports/summary_statement_recruiter.html'
    def get(self, request):
        args = {}
        args['form'] = SummaryStatementRecruimentForm()
        return render_to_response(self.template, RequestContext(request, args))

    def post(self, request):
        vacancies = json.loads(request.POST['vacancies'])
        period = request.POST['period'].split('/')
        print vacancies

        document_rows = []

        header = [
            [u'Вакансия', ''],
            [u'Дата открытия/ возобновления'],
            [u'Источник размещения'],
            [u'Всего обращений (звонки, резюме, отклики, прозвон соискателей)'],
            [
                {u'1-ое собеседование':[
                        [u'Приглашены'],
                        [u'Пришли']
                    ]
                }
            ],
            [
                {u'1-ое собеседование':[
                        [u'Приглашены'],
                        [u'Пришли']
                    ]
                }
            ],
            [
                {u'Первая неделя / ИС':[
                        [u'Приглашены'],
                        [u'Отказались/ не вышли'],
                        [u'Думают'],
                        [u'Вышли'],
                        [u'Прошли первую неделю/ работают на ИС'],
                    ]
                }
            ]
        ]

        document_rows.append(header)