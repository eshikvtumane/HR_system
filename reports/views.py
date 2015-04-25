#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.views.generic import View

from vacancies.models import ApplicantVacancy, Vacancy, ApplicantVacancyApplicantVacancyStatus, VacancyStatusHistory, Position, Department
from applicants.models import SourceInformation

from forms import SummaryStatementRecruimentForm, PositionStatementForm
from datetime import datetime, timedelta
from dateutil import relativedelta as rdelta
import json
import xlwt

from django.db.models import Q

import pprint

# Create your views here.
'''
    CONSTANTS
'''
MONTH = {
    '01':u'Январь',
    '02':u'Февраль',
    '03':u'Март',
    '04':u'Апрель',
    '05':u'Май',
    '06':u'Июнь',
    '07':u'Июль',
    '08':u'Август',
    '09':u'Сентябрь',
    '10':u'Октябрь',
    '11':u'Ноябрь',
    '12':u'Декабрь'
}

class MainReports(View):
    template = 'reports/reports.html'
    def get(self, request):
        return render_to_response(self.template, RequestContext(request))


class GenerateReport():
    def __init__(self):
        self.wb = xlwt.Workbook(encoding='utf-8')
        self.depth = 0
        self.body_depth = 0

    def createWorksheet(self, sheet_name):
        return self.wb.add_sheet(sheet_name, cell_overwrite_ok=True)

    def getWorksheet(self):
        return self.wb

    def writeValues(self, ws, row_start, column_start, values, empty_value='-'):

        for value in values:
            if len(value) == 2:
                style = value[1]
            else:
                style = ''

            text = unicode(value[0])
            if text == u'0' or text == u'':
                text = empty_value
            ws.write(row_start, column_start, text, self.__applyStyle(style))

            column_start += 1

    def writeMerge(self, ws, row_start, row_end, column_start, column_end, value, style=''):
        ws.write_merge(row_start, row_end, column_start, column_end, value, self.__applyStyle(style))

    def writeMergeList(self, ws, row_start, row_end, column_start, column_end, values, style=''):
        for count, value in enumerate(values):
            try:
                text = unicode(value[0])
            except:
                text = value[0]

            if text != u'':
                ws.write_merge(row_start+count, row_end+count, column_start, column_end, text, self.__applyStyle(style))


    def writeHeader(self, sheet, header, row_start, column_start=0):
        row_start -= 1
        self.writeHead(sheet, header, row_start, column_start)

        row_end = self.depth + row_start - 1
        self.mergeColumn(sheet, header, row_start, column_start, row_end)

        #self.writeBody(sheet, body, row_end + 1, column_start)
        return row_end + 1


    def writeHead(self, ws, values, row_start, column_start, depth=0):
        dict_count = 0
        list_count = 0

        depth += 1
        total_length = 0
        current_length = len(values)
        for value in values:
            try:
                style = self.__applyStyle(value[1])
                style_buf = value[1]
            except Exception, e:
                style = self.__applyStyle('')
                style_buf = ''

            if isinstance(value[0], dict):
                length = self.writeHead(ws, value[0].values()[0], row_start+1, column_start, depth)

                column_end = column_start - 1 + length

                ws.write_merge(row_start, row_start, column_start, column_end, value[0].keys()[0], style)

                column_start = column_end

                total_length += length

                dict_count += 1
            else:
                text = unicode(value[0])

                if text == u'0':
                    ws.write(row_start, column_start, '-', style)
                else:
                    ws.write(row_start, column_start, text, style)

                    size = 0
                    if 'align: rotation 90' in style_buf or 'align:rotation 90' in style_buf:
                        size = len(text.split('\n')) + 1
                    else:
                        text_list = text.split('\n')
                        for text in text_list:
                            text_length = len(text)
                            if size < text_length:
                                size = text_length

                    self.autoResizeColumnWidth(ws, column_start, size + 4)

                list_count += 1

            column_start += 1

        if self.depth < depth:
            self.depth = depth

        if current_length > total_length:
            total_length += current_length

        if dict_count != 0 and list_count != 0:
            total_length += list_count

        return total_length

    def writeBody(self, ws, values, row_start, column_start, depth=0):
        dict_count = 0
        list_count = 0

        depth += 1
        total_length = 0
        current_length = len(values)
        for value in values:
            try:
                style = self.__applyStyle(value[1])
            except Exception, e:
                style = self.__applyStyle('')

            if isinstance(value[0], dict):
                length = self.writeBody(ws, value[0].values()[0], row_start, column_start+1, depth)

                row_end = row_start - 1 + length

                ws.write_merge(row_start, row_end, column_start, column_start, value[0].keys()[0], style)

                row_start = row_end

                total_length += length

                dict_count += 1
            else:
                text = value[0]
                ws.write(row_start, column_start, text, style)

                list_count += 1

            row_start += 1

        if self.depth < depth:
            self.depth = depth

        if current_length > total_length:
            total_length += current_length

        if dict_count != 0 and list_count != 0:
            total_length += list_count

        return total_length

    def mergeColumn(self, ws, values, row_start, column_start, row_end):
        dict_count = 0
        list_count = 0

        total_length = 0
        current_length = len(values)
        for value in values:
            if isinstance(value[0], dict):
                length = self.mergeColumn(ws, value[0].values()[0], row_start+1, column_start, row_end)

                column_end = column_start - 1 + length
                column_start = column_end

                total_length += length

                dict_count += 1
            else:
                ws.merge(row_start, row_end, column_start, column_start)
                list_count += 1
            column_start += 1

        if current_length > total_length:
            total_length += current_length

        if dict_count != 0 and list_count != 0:
            total_length += list_count

        return total_length

    def write_column(self, ws, row, col, values):
        for value in values:
            ws.write(row, col, value[0], self.__applyStyle(value[1]))
            row += 1
        return row

    def __applyStyle(self, style):
        return xlwt.easyxf(style)

    def autoResizeRowHeight(self, sheet, row_number, size):
        row = sheet.row(row_number - 1)
        row.height_mismatch = True
        row.height = 256 * size

    def autoResizeColumnWidth(self, sheet, column_number, size):
        sheet.col(column_number).width = 256 * size


    def saveWorkbook(self, name='report.xls'):
        self.wb.save(name)

    def saveWorkbookInResponse(self, name='report'):
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s.xls' % name
        self.saveWorkbook(response)
        return response

class CellStyle():
    def __init__(self):
        self.align_vert = 'align: vert center;'
        self.align_horiz = ' align: horiz center;'
        self.border = 'borders: bottom thin, top thin, left thin, right thin;'
        self.align = self.align_vert + self.align_horiz

    def alignCenterBold(self):
        header_style_horiz = self.align + 'font: bold on;' + self.border
        return header_style_horiz

    def alignCenter(self):
        return self.align + self.border

class DateRange():
    def dateRange(self, dismissal, hiring_day):
        return self.dateString(rdelta.relativedelta(dismissal, hiring_day))

    def dateString(self, period):
        print 'period', period
        years = period.year
        months = period.months
        days = period.days


        year_words = [
            u'год',
            u'года',
            u'лет'
        ]
        month_words = [
            u'месяц',
            u'месяца',
            u'месяцев',
        ]
        day_words = [
            u'день',
            u'дня',
            u'дней'
        ]

        result = self.__getDeclension(years, year_words) + \
                self.__getMonthDeclension(months, month_words) + \
                self.__getDeclension(days, day_words)

        return u' '.join(result)

    def __getDeclension(self, number, word_list):
        string_list = []
        if number != 0 and isinstance(number, int):
            number = str(number)
            number_len = len(number)
            int_number = int(number[number_len-1])
            string_list.append(number)
            if int_number == 1:
                string_list.append(word_list[0])
            elif int_number > 1 and int_number < 5:
                string_list.append(word_list[1])
            else:
                string_list.append(word_list[2])
        return string_list

    def __getMonthDeclension(self, number, word_list):
        string_list = []
        if number != 0 and isinstance(number, int):
            number = str(number)
            number_len = len(number)
            int_number = int(number[number_len-1])
            int_number_two = int(number[number_len-2:])
            string_list.append(number)

            if int_number_two >= 10 and int_number_two <= 20:
                string_list.append(word_list[2])
            elif int_number == 1:
                string_list.append(word_list[0])
            elif int_number > 1 and int_number < 5:
                string_list.append(word_list[1])
            else:
                string_list.append(word_list[2])
        return string_list

# Сводная ведомость по набору персонала
class SummaryStatementRecruitment(View):
    template = 'reports/summary_statement_recruiter.html'
    def get(self, request):
        args = {}
        args['form'] = SummaryStatementRecruimentForm()
        return render_to_response(self.template, RequestContext(request, args))

class SummaryStatementRecruitmentGenerateAjax(View):
    def get(self, request):
        '''
            Стили для значений в ячейках
        '''
        align_vert = 'align: vert center;'
        align_horiz = ' align: horiz center;'
        align = align_vert + align_horiz
        border = 'borders: bottom thin, top thin, left thin, right thin;'

        header_style_horiz = align + 'font: bold on;' + border
        header_style_vert = 'align: rotation 90;' + 'font: bold on;' + align + border
        style_horiz = align  + border

        gp = GenerateReport()
        sheet = gp.createWorksheet(u'Ведомость')


        header = [
            [u'Вакансия', header_style_horiz],
            [u'Дата открытия/ \nвозобновления', header_style_horiz],
            [u'Источник \nразмещения', header_style_horiz],
            [u'Всего обращений \n(звонки, резюме, \nотклики, прозвон \nсоискателей)', header_style_horiz],
            [
                {u'1-ое собеседование':[
                        [u'Приглашены', header_style_horiz],
                        [u'Пришли', header_style_horiz]
                    ]
                },
                header_style_horiz
            ],
            [
                {u'2-ое собеседование':[
                        [u'Приглашены', header_style_horiz],
                        [u'Пришли', header_style_horiz]
                    ]
                }, header_style_horiz
            ],
            [
                {u'Дополнительное\nсобеседование':[
                        [u'Приглашены', header_style_horiz],
                        [u'Пришли', header_style_horiz]
                    ]
                }, header_style_horiz
            ],
            [
                {u'Первая неделя / ИС':[
                        [u'Приглашены', header_style_vert],
                        [u'Отказались/ \nне вышли', header_style_vert],
                        [u'Думают', header_style_vert],
                        [u'Вышли', header_style_vert],
                        [u'Прошли \nпервую неделю/ \nработают на ИС', header_style_vert],
                    ]
                }, header_style_horiz
            ]
        ]

        column_start = 0


        row_start = gp.writeHeader(sheet, header, 3, 0)
        body = self.getData(request, row_start, column_start, gp, sheet, style_horiz)


        gp.autoResizeColumnWidth(sheet, 0, 23)
        gp.autoResizeRowHeight(sheet, 3, 2)
        gp.autoResizeRowHeight(sheet, 4, 7)

        sheet.portrait = False
        sheet.set_fit_num_pages(1)
        sheet.header_str = ''
        sheet.footer_str = ''
        return gp.saveWorkbookInResponse()


    def getData(self, request, row_start, column_start, gp, sheet, style=''):
        total_style = style + 'font: bold on;'
        total_title_style = 'font: bold on;' + ' align: horiz right;'
        color_cell = 'pattern: pattern solid, fore_colour yellow;'


        request = request.GET
        vacancies = json.loads(request['vacancies'])
        period = request['period'].split('/')


        # Заголовок отчёта
        title_style = 'align: horiz center;' + 'font: bold on;'
        title_text = 'Сводная ведомость по набору персонала за {0} {1} г.'.format(MONTH[period[0]].lower().encode('utf-8'), period[1].encode('utf-8'))
        gp.writeMerge(sheet, 0, 0, 0, 14, title_text, title_style)

        # Сохранение причин отказов от работы
        rejection_list = []

        # счётчик сносок
        reserve_count = 1
        # список людей, вышедших на работу с резерва
        reserve_info_list = []

        total_sums = [[0, total_style] for i in xrange(12)]

        count = 0
        # выбераем вакансии (присланные с клиента) из массива
        for key in vacancies:
            # получение данных о вакансии
            vacancy_id = vacancies[key]['vacancy']
            vacancy = Vacancy.objects.get(pk=vacancy_id)
            # получение данных о кандидатах, претендующих на эту вакансию
            vacancy_sources = ApplicantVacancy.objects.filter(
                vacancy=vacancy
            )

            sources = vacancies[key]['source']

            result_vacancy = []


            vacancy_statuses = VacancyStatusHistory.objects.filter(vacancy=vacancy_id).values('status__name', 'date_change')
            vacancy_open = vacancy_statuses[0]

            if vacancy_statuses.count() == 1:
                vacancy_status_str =u'%s с \n %s' % (vacancy_open['status__name'], vacancy_open['date_change'].date())
            else:
                vacancy_change = vacancy_statuses.latest('status')
                vacancy_status_str =u'%s с \n %s \ \n %s с \n %s' % (vacancy_open['status__name'], vacancy_open['date_change'].date(),
                                                                    vacancy_change['status__name'], vacancy_change['date_change'].date()
                                                                    )


            # форматирование текста
            position = vacancy.position.name.split(' ')
            str_len = 23
            result_position = ''
            buf_position = ''

            for pos in position:
                if len(buf_position + pos) <= str_len:
                    buf_position =  buf_position + ' ' + pos
                    result_position += ' ' + pos
                else:
                    result_position += '\n' + buf_position
                    buf_position = ' ' + pos

            sources_len = len(sources) - 1
            gp.writeMerge(sheet, row_start, row_start+sources_len, column_start, column_start, result_position, style)
            gp.writeMerge(sheet, row_start, row_start+sources_len, column_start + 1, column_start + 1, vacancy_status_str, style)


            # сбор статистики по источникам
            for source in sources:
                # хранение количества людей по всем позициям(например, приглашены, пришли, думают и др.)
                result_counter = []

                # получение инофрмации об источнике
                source_obj = SourceInformation.objects.get(pk=source)
                source_name = source_obj.source
                result_counter.append([source_name, style])

                # выборка статусов по вакансию
                result_status = ApplicantVacancyApplicantVacancyStatus.objects.filter(
                                                        applicant_vacancy__vacancy = vacancy,
                                                        applicant_vacancy__source=source_obj,
                                                        date__month=period[0],
                                                        date__year=period[1]
                )

                # выборка всех статусов по вакансии с определённого источника за определённый период
                '''vacancy_info = vacancy_sources.filter(source=source_obj,
                                                      date_created__month=period[0],
                                                      date_created__year=period[1]
                )'''
                # общее количество заявок по вакансии из данного источника ()
                #total_count = result_status.distinct('applicant_vacancy__applicant').count()
                total_count = result_status.count()

                # если нет заявок, то дальнейшую выборку не производим
                if total_count != 0:
                    # Добавляем общее количество заявок с данного источника
                    result_counter.append([total_count, style])

                    # 1-е собеседование
                    # Приглашены
                    first_interview = result_status.filter(applicant_vacancy_status__name__contains='1-е собеседование запланировано').count()
                    result_counter.append([first_interview, style])
                    # Пришли
                    first_went = result_status.filter(applicant_vacancy_status__name__contains='1-е собеседование состоялось').count()
                    result_counter.append([first_went, style])

                    # 2-е собеседование
                    # Приглашены
                    second_interview = result_status.filter(applicant_vacancy_status__name__contains='2-е собеседование запланировано').count()
                    result_counter.append([second_interview, style])
                    # Пришли
                    second_went = result_status.filter(applicant_vacancy_status__name__contains='2-е собеседование состоялось').count()
                    result_counter.append([second_went, style])

                    # Дополнительное собеседование
                    # Приглашены
                    ext_interview = result_status.filter(applicant_vacancy_status__name__contains='Дополнительное собеседование запланировано').count()
                    result_counter.append([ext_interview, style])
                    # Пришли
                    ext_went = result_status.filter(applicant_vacancy_status__name__contains='Дополнительное собеседование состоялось').count()
                    result_counter.append([ext_went, style])
                else:
                    result_counter = [[source_name, style]] + [[0, style]] * 7


                # Приглашены
                buf = result_status.filter(applicant_vacancy_status__name__contains='Предложение кандидату').count()
                result_counter.append([buf, style])

                # Отказались/не вышли
                rejection = result_status.filter(Q(applicant_vacancy_status__name__contains='Самоотказ') |
                                                 Q(applicant_vacancy_status__name__contains='Предложение отклонено') |
                                                 Q(applicant_vacancy_status__name__contains='Не вышли')
                ).values('note')

                rejection_count = rejection.count()
                result_counter.append([rejection_count, style])

                # сохранение причин отказа от работы
                for r in rejection:
                    rejection_list.append([r['note']])

                # Думают
                result_counter.append([
                    result_status.filter(applicant_vacancy_status__name__contains='Сделано предложение').count(),
                    style
                ])
                '''
                    Вышли
                '''
                # люди, которые вышли на работу
                went_to_work = result_status.filter(applicant_vacancy_status__name__contains='Вышел')
                # выборка людей, которые вышли на работу с резерва
                applicants = went_to_work.values('applicant_vacancy__applicant', 'applicant_vacancy__vacancy')
                reserve = []
                for i in applicants:
                    reserve = result_status.filter(applicant_vacancy__applicant=i['applicant_vacancy__applicant'],
                                                  applicant_vacancy__vacancy=i['applicant_vacancy__vacancy'],
                                                  applicant_vacancy_status__name__contains='Резерв')\
                        .values('applicant_vacancy__applicant__first_name',
                              'applicant_vacancy__applicant__last_name',
                              'applicant_vacancy__applicant__middle_name',
                              'applicant_vacancy__vacancy__head__name',
                              'applicant_vacancy__vacancy__published_at',
                              'date'
                            )



                # Формирование сноски с информацией о людях из резерва                                                                              )

                if len(reserve) != 0:
                    result_counter.append([went_to_work.count(), style + color_cell])
                    print 'Reserve', len(reserve), reserve.count(), reserve
                    for r in reserve:
                        reserve_info_list.append(['%s, %s, рук. %s - резерв с %s - %s %s %s' % (vacancy.position.name.encode("utf-8"),
                                                              source_name.encode("utf-8"),
                                                               r['applicant_vacancy__vacancy__head__name'].encode("utf-8"),
                                                              r['date'].date(),
                                                              r['applicant_vacancy__applicant__first_name'].encode("utf-8"),
                                                               r['applicant_vacancy__applicant__last_name'].encode("utf-8"),
                                                               r['applicant_vacancy__applicant__middle_name'].encode("utf-8")
                                                )
                        ])
                        reserve_count += 1
                else:
                    result_counter.append([went_to_work.count(), style])

                # -----------------------------------------------------------------------

                '''
                    Прошли первую неделю/работают на ИС
                '''
                result_counter.append([
                    result_status.filter(Q(applicant_vacancy_status__name__contains='Испытательный срок') |
                                    Q(applicant_vacancy_status__name__contains='Прошли первую рабочую неделю')

                    ).count(),
                    style
                    ]
                )



                for count, rs in enumerate(result_counter[1:]):
                    total_sums[count][0] += rs[0]

                gp.writeValues(sheet, row_start, column_start+2, result_counter)
                row_start += 1


        gp.writeMerge(sheet, row_start, row_start, 0, 2, u'Итого', total_title_style)
        gp.writeValues(sheet, row_start, 3, total_sums)

        gp.writeMerge(sheet, row_start+2, row_start+2, 0, 4, 'Вышли на работу с резерва:', color_cell)
        gp.writeMergeList(sheet, row_start+3, row_start+3, 0, 4, reserve_info_list,  '')

        # Причины отказа
        gp.writeMerge(sheet, row_start+2, row_start+2, 6, 12, 'Причины отказа от предложений по работе:', '')
        gp.writeMergeList(sheet, row_start+3, row_start+3, 6, 13, rejection_list, '')
        return

class PositionStatement(View, DateRange):
    template = 'reports/position_statement.html'
    def get(self, request):
        args = {}
        args['form'] = PositionStatementForm()
        return render_to_response(self.template, RequestContext(request, args))

    def post(self, request):
        style = CellStyle()
        year = request.POST['year']
        position = request.POST['position']

        gp = GenerateReport()
        sheet = gp.createWorksheet(u'Информация по персоналу')
        column_start = 0
        row_start = 0

        sheet.set_fit_num_pages(1)
        sheet.header_str = ''
        sheet.footer_str = ''

        position_obj = Position.objects.get(pk=position)

        title = '%s - %s' % (position_obj.name.upper(), year)
        title_style = 'align: horiz center;' + 'font: bold on;'

        style_header = style.alignCenterBold()
        header = [
            [u'№', style_header],
            [u'ФИО', style_header],
            [u'Руководитель', style_header],
            [u'Дата приёма', style_header],
            [u'Дата \r\n увольнения', style_header],
            [u'Период / \r\n срок работы', style_header],
            [u'Отзыв', style_header]
        ]

        gp.writeMerge(sheet, row_start, row_start, column_start, column_start+len(header)-1, title, title_style)
        row_start += 3
        gp.writeHeader(sheet, header, row_start, 0)
        gp.autoResizeRowHeight(sheet, row_start, 2)
        gp.autoResizeColumnWidth(sheet, 1, 30)

        statuses = ApplicantVacancyApplicantVacancyStatus.objects.filter(applicant_vacancy__vacancy=position_obj,
                                                                            date__year = year)

        applicants = statuses.filter(applicant_vacancy_status__name__contains='Принят на работу')\
            .values('applicant_vacancy__applicant',
                      'applicant_vacancy__vacancy',
                      'applicant_vacancy__vacancy__head__name',
                      'applicant_vacancy_status__name',
                      'applicant_vacancy__applicant__first_name',
                      'applicant_vacancy__applicant__last_name',
                      'applicant_vacancy__applicant__middle_name',
                      'applicant_vacancy__vacancy__published_at',
                      'date'
                    )


        style_body = style.alignCenter()
        for count, i in enumerate(applicants):
            try:
                result = statuses.get(applicant_vacancy__applicant=i['applicant_vacancy__applicant'],
                                              applicant_vacancy_status__name__contains='Уволен')\
                    .values('date', 'note')
            except:
                result = None


            hiring_day = i['date'].date()
            if result:
                dismissal = result.date.date()
                period = self.dateRange(dismissal, hiring_day)
            else:
                period = self.dateRange(datetime.now(), hiring_day)
                dismissal = '-'


            if isinstance(result, ApplicantVacancyApplicantVacancyStatus) and result.note.rstrip():
                characteristics = 'да'
            else:
                characteristics = ''

            employer = [
                [count+1, style_body],
                ['%s %s %s' % (i['applicant_vacancy__applicant__first_name'],
                                i['applicant_vacancy__applicant__last_name'],
                                i['applicant_vacancy__applicant__middle_name']
                ), style_body],
                [i['applicant_vacancy__vacancy__head__name'], style_body],
                [hiring_day, style_body],
                [dismissal, style_body],
                [period, style_body],
                [characteristics, style_body]
            ]

            gp.writeValues(sheet, row_start, 0, employer)
            row_start += 1
        return gp.saveWorkbookInResponse()




class VacancyReport(View):
    template = 'reports/vacancy_reports.html'
    def get(self, request):
        args = {}
        args['form'] = SummaryStatementRecruimentForm()
        rc = RequestContext(request, args)
        return render_to_response(self.template, rc)

class VacancyReportGenerateAjax(View, DateRange):
    def get(self, request):
        '''
            Стили для значений в ячейках
        '''
        align_vert = 'align: vert center;'
        align_horiz = ' align: horiz center;'
        align = align_vert + align_horiz
        border = 'borders: bottom thin, top thin, left thin, right thin;'

        header_style_horiz = align + 'font: bold on;' + border
        header_style_vert = 'align: rotation 90;' + 'font: bold on;' + align + border
        header_style = align + 'font: bold on;'
        style_bold = align + border + 'font: bold on;'
        style_horiz = align + border

        color_cell = 'pattern: pattern solid, fore_colour yellow;'
        #'font: colour white, bold True;'

        gp = GenerateReport()
        sheet = gp.createWorksheet(u'Ведомость')

        header = [
            [u'№', header_style_horiz],
            [u'Вакансия', header_style_horiz],
            [u'Количество', header_style_horiz],
            [u'Дата открытия\nвакансии', header_style_horiz],
            [u'Дата\nприостановления/\nснятия вакансии', header_style_horiz],
            [u'Руководитель отдела', header_style_horiz]

        ]

        header2 = [
            [u'№', header_style_horiz],
            [u'Вакансия', header_style_horiz],
            [u'Количество', header_style_horiz],
            [u'Дата открытия\nвакансии', header_style_horiz],
            [u'Дата\nзакрытия вакансии', header_style_horiz],
            [u'Заявка на подбор', header_style_horiz],
            [u'Период\nподбора', header_style_horiz],
            [u'Ф.И.О. принятого\nсотрудника', header_style_horiz]
        ]

        header_len = len(header2)
        period = request.GET['period'].encode('utf-8')
        report_date = datetime.strptime(period, '%d-%m-%Y') + timedelta(days=1)

        gp.writeMerge(sheet, 0, 0, 0, 1, 'на %s' % period, '')
        gp.writeMerge(sheet, 1, 1, 0, header_len - 1, 'ОТКРЫТЫЕ ВАКАНСИИ', header_style)
        row_start = gp.writeHeader(sheet, header, 4, 0)

        row_start2 = row_start + 2
        gp.writeMerge(sheet, row_start2, row_start2, 0, header_len - 1, 'ЗАКРЫТЫЕ ВАКАНСИИ', header_style)
        row_start = gp.writeHeader(sheet, header2, row_start2 + 3, 0)
        gp.autoResizeRowHeight(sheet, row_start2 + 3, 3)

        count_vacancy = 0
        positions = Position.objects.all()
        departments = Department.objects.all()

        # выборка открытых вакансий


        # выборка закрытых вакансий
        total_vacancies = 0
        # выбор отделов
        for department in departments:
            # место для названия отдела
            department_row_start = row_start
            row_start += 1

            # счётчик закрытых вакансий
            closed_count = 0
            # выбор должностей, относящихся к отделу
            for position in positions:
                vacancies = Vacancy.objects.filter(position=position, head__department=department)
                # перебор вакансий
                for vacancy in vacancies:
                    # поиск закрытых вакансий
                    closed = VacancyStatusHistory.objects.filter(vacancy=vacancy).filter(status__name='Закрыта', date_change__lte=report_date)
                    row_start_buf = row_start

                    if closed.count():
                        for close_vac in closed:
                            open = VacancyStatusHistory.objects.filter(Q(vacancy=close_vac.vacancy) & \
                                                                       Q(date_change__lte=report_date) & \
                                                                       (Q(status__name='Открыта') | \
                                                                        Q(status__name='Возоблена'))).latest('status')

                            # период подбора
                            period = self.dateRange(close_vac.date_change, open.date_change)
                            result = [
                                1,
                                open.date_change.strftime('%d-%m-%Y'),
                                close_vac.date_change.strftime('%d-%m-%Y'),
                                close_vac.vacancy.head.name,
                                period
                            ]
                            # общее количество закрытых вакансий
                            total_vacancies += 1

                            # принятые кандидаты
                            applicants = ApplicantVacancyApplicantVacancyStatus.objects.filter(applicant_vacancy__vacancy=close_vac.vacancy,applicant_vacancy_status__name__contains='Принят на работу')

                            applicant_name = []
                            for applicant in applicants:
                                a = applicant.applicant_vacancy.applicant
                                name = '%s %s.' % (a.first_name, a.last_name[0])
                                if a.middle_name:
                                    name += a.middle_name[0] + '.'

                                # уволенные кандидаты
                                fired = ApplicantVacancyApplicantVacancyStatus.objects.filter(applicant_vacancy__applicant=a,applicant_vacancy__vacancy=close_vac.vacancy,applicant_vacancy_status__name__contains='Уволен').count()
                                if fired:
                                    applicant_name.append([name, style_horiz + color_cell])
                                else:
                                    applicant_name.append([name, style_horiz])

                            # запись в файл  кандидатов
                            row_end = gp.write_column(sheet, row_start, 7, applicant_name)

                            for count, r in enumerate(result):
                                gp.writeMerge(sheet, row_start, row_end-1, count+2, count+2, r, style_horiz)
                            row_start = row_end

                            closed_count += 1

                    # если есть закрытые вакансии, то записываем в файл
                    if row_start_buf <= row_start-1:
                        count_vacancy += 1
                        gp.writeMerge(sheet, row_start_buf, row_start-1, 0, 0, count_vacancy, style_horiz)
                        gp.writeMerge(sheet, row_start_buf, row_start-1, 1, 1, position.name, style_horiz)

            # если закрытых вакансий в отделе нет, то и название отдела не записываем
            if closed_count == 0:
                row_start -= 1
            else:
                gp.writeMerge(sheet, department_row_start, department_row_start, 0, header_len - 1, department.name, header_style_horiz)

        # итого
        gp.writeMerge(sheet, row_start, row_start, 0, 1, 'Закрыто', style_bold)
        gp.writeMerge(sheet, row_start, row_start, 2, 2, total_vacancies, style_horiz)
        # примечание
        gp.writeMerge(sheet, row_start+2, row_start+2, 1, 1, "ФИО", style_horiz + color_cell)
        gp.writeMerge(sheet, row_start+2, row_start+2, 2, 2, "- уволен", '')

        #gp.autoResizeColumnWidth(sheet, 0, 23)
        #gp.autoResizeRowHeight(sheet, 3, 2)
        gp.autoResizeRowHeight(sheet, 4, 4)

        #sheet.portrait = False
        sheet.set_fit_num_pages(1)
        sheet.header_str = ''
        sheet.footer_str = ''
        return gp.saveWorkbookInResponse()

