#-*- coding:utf8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.core.exceptions import ValidationError

from django.views.generic import View
from django.template import RequestContext
from django.http import HttpResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from forms import ApplicantForm, CandidateSearchForm, ApplicantEducationForm, VacancyForm
from models import Education, Major, SourceInformation, Applicant, Resume, Portfolio, Position, Phone, ApplicantEducation, HistoryChangeApplicantInfo
from vacancies.models import Vacancy, ApplicantVacancy, \
    ApplicantVacancyStatus, CurrentApplicantVacancyStatus, VacancyStatusHistory

from events.models import ApplicantVacancyEvent
from vacancies.forms import ApplicantVacancyEventForm
from django.contrib.auth.models import User

import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

import json

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


import datetime


import bleach
from django.db.models import Q
import operator

# Create your views here.

class SavingModels():

    def sourceCreate(self, source):
        try:
            convert_id = int(source)
            return SourceInformation.objects.get(pk=convert_id)
        except:
            if source:
                source_obj = SourceInformation(source=source, author=self.author)
                source_obj.save()
                return source_obj
        return

    def createMajor(self, major):
        try:
            convert_id = int(major)
            return convert_id
        except:
            major_obj = Major(name=major, author=self.author)
            major_obj.save()
            return major_obj.id

    def savingPhone(self, phones, user):
        try:
            phone_obj = []
            if phones:
                for p in phones:
                    if p != '':
                        # удаление ненужных символов
                        chars_to_remove = ['(', ')', ' ', '‒'.decode('unicode_escape').encode('ascii','ignore'), '-']
                        phone = self.replaceLetters(p, chars_to_remove)
                        phone_obj.append(Phone(applicant=user, phone=phone))

                Phone.objects.bulk_create(phone_obj)

            return
        except Exception, e:
            print '%s %s' % ('Save phone number error', e.message)
            return

    def savingVacancies(self, json_vacancies, user, req_user):
        try:
            vacancies = json.loads(json_vacancies)
            vacancy_obj = []


            for k, v in enumerate(vacancies):
                vacancies[v]['vacancy'] = Vacancy(vacancies[v]['vacancy'])
                vacancies[v]['applicant'] = user
                vacancies[v]['source'] = self.sourceCreate(vacancies[v]['source'])

                #CurrentApplicantVacancyStatus(applicant_vacancy=)
                vacancy_obj.append(ApplicantVacancy(**vacancies[v]))

            ApplicantVacancy.objects.bulk_create(vacancy_obj)
            new_applicant_vacancies = ApplicantVacancy.objects.all().order_by('-id')[:len(vacancies)]
            new_applicant_vacancy_statuses = []

            # добавление статуса по умолчанию
            for a in new_applicant_vacancies:
                new_applicant_vacancy_statuses.append(CurrentApplicantVacancyStatus(
                                                    applicant_vacancy=a,\
                                                    applicant_vacancy_status=ApplicantVacancyStatus.objects.get(name__contains='Новый кандидат'),\
                                                    date = datetime.datetime.now(),
                                                    author=req_user))

                CurrentApplicantVacancyStatus(
                                                    applicant_vacancy=a,\
                                                    applicant_vacancy_status=ApplicantVacancyStatus.objects.get(name__contains='Новый кандидат'),\
                                                    author=req_user,\
                                                    note='').save()

            return
        except Exception, e:
            print 'Error 2'
            print e.message
        return

    def savingEducations(self, json_educations, user):
        print '111', json_educations
        try:
            educations = json.loads(json_educations['educations'])
            edu_obj = []
            print educations
            for k, v in enumerate(educations):
                educations[v]['education'] = Education.objects.get(pk=educations[v]['education'])
                educations[v]['major'] = Major.objects.get(pk=self.createMajor(educations[v]['major']))
                educations[v]['applicant'] = user
                edu_obj.append(ApplicantEducation(**educations[v]))

            ApplicantEducation.objects.bulk_create(edu_obj)
        except Exception, e:
            print 'Error 1'
            print e.message
        return

    # добавление изменения анкеты кандидата
    def addHistoryChange(self, user, applicant, type):
        hcai = HistoryChangeApplicantInfo(
            user=user,
            applicant=applicant,
            type_change=type
        )
        hcai.save()

        return

    def addForms(self, applicant_instance={}):
        args = {}
        args['applicant_form'] = ApplicantForm(**applicant_instance)
        args['edu_form'] = ApplicantEducationForm()
        args['vacancy_form'] = VacancyForm()
        args['event_form'] = ApplicantVacancyEventForm()
        #args['positions'] = Position.objects.all()
        #args['sources'] = SourceInformation.objects.all()

        return args

    def savingApplicantForm(self, request, type_change, applicant_instance={}):
        #try:
        req = request.POST
        self.author = request.user
        # создание объекта класса сохранения файлов
        sf = SavingFiles()

        # удаляем полный адрес
        del req['fullname']

        # конвертирование даты в формат, понятный БД
        if req['birthday'] != '__-__-____':
            try:
                if req['birthday']:
                    req['birthday'] = datetime.datetime.strptime(req['birthday'], "%d-%m-%Y").date()
            except:
                req['birthday'] = datetime.datetime.strptime(req['birthday'], "%Y-%m-%d").date()

        # сохранение данных в таблицу Applicant
        # сохраниение нового источника или получение id существующего источника
        #request.POST['source'] = self.sourceCreate(req['source'])

        if req['icq']:
            req['icq'] = int(req['icq'])
        else:
            req['icq'] = None


        applicant_form = ApplicantForm(request.POST, request.FILES, **applicant_instance)
        if applicant_form.is_valid():
            new_applicant = applicant_form.save()
        else:
            print applicant_form.errors
            return False

        try:
            del req['street']
            del req['city']
            del req['building']
        except Exception, e:
            print 'Error on delete key: ' + e.message;

        self.savingPhone(req.getlist('phone'), new_applicant)
        self.savingVacancies(req['vacancies'], new_applicant, request.user)
        print '555'
        #req['educations'] = req.get('educations' or None)
        #if req['educations']:
        self.savingEducations(req, new_applicant)


        full_name = new_applicant.getFullName()

        resume = sf.saveFiles(request.FILES.getlist('resume[]'),
                              dir='resume',
                              filename=full_name)
        portfolio = sf.saveFiles(request.FILES.getlist('portfolio[]'),
                                 dir='portfolio',
                                 filename=full_name)

        # сохранение текстовых файлов с резюме и запись ссылки в БД
        if resume:
            # запись файлов на сервер
            resume_list = [Resume(applicant = new_applicant, resume_file = r) for r in resume]
            # сохранение ссылок на файлы в таблицу
            Resume.objects.bulk_create(resume_list)
        # сохранение архивов с работами кандидата и запись ссылки в БД
        if portfolio:
            # запись файлов на сервер
            portfolio_list = [Portfolio(applicant = new_applicant, portfolio_file = p) for p in portfolio]
            # сохранение ссылок на файлы в таблицу
            Portfolio.objects.bulk_create(portfolio_list)

        # добавление изменения в историю
        self.addHistoryChange(request.user, new_applicant, type_change)
        return new_applicant.id
        '''except Exception, e:
            print 't'
            print e.message
            return False'''

    # удаление ненужных символов
    def replaceLetters(self, word, letters):
        word = word.encode('utf8')
        result = ''
        for letter in word:
            if letter not in letters:
                result += letter.decode('unicode_escape').encode('ascii','ignore')
        return result

    def render(self, request, result_list, total_count=0):
        return self.paginator(request, result_list)





class ApplicantAddView(View, SavingModels):
    '''
        Добавление кандидата
    '''
    template = 'applicants/applicant_add.html'

    @method_decorator(login_required)
    def get(self, request):
        args = self.addForms()

        rc = RequestContext(request, args)
        return render_to_response(self.template, rc)

    @method_decorator(login_required)
    def post(self, request):
        if request.is_ajax:
            result = self.savingApplicantForm(request, 'Создан')
            json_res = json.dumps(['200',result])
        else:
            json_res = json.dumps(['200'])

        return HttpResponse(json_res, 'application/json')


class SavingFiles():
    '''
        сохранение файлов
    '''

    def saveFiles(self, files, dir='', path=settings.MEDIA_URL, filename=''):
        arr_path = []
        for f in files:
            arr_path.append(self.__save(f, dir, path, filename))
        return arr_path

    def __save(self, f,  dir, path, filename):
        original_name, file_extension = os.path.splitext(f.name)
        filename = filename + '-' + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + file_extension

        save_path = default_storage.save(os.path.join(dir, filename), ContentFile(f.read()))
        file_url = os.path.join(path, save_path)
        return file_url

class VacancySearchAjax(View):
    '''
        выборка вакансий
    '''
    def get(self, request):
        if request.is_ajax:
            position = request.GET.get('position')
            '''vacancies = Vacancy.objects.filter(Q(position=position) &\
                                                           (Q(last_status__name__contains='Открыта') |\
                                                            Q(last_status__name__contains='Возобновлена')))\
                                                            .values('head__name', 'id', 'published_at')'''
            vacancies = Vacancy.objects.filter(position=position).values('head__name', 'id', 'published_at', 'last_status__name')
            result = [
                {
                    'head': v['head__name'],
                     'date': v['published_at'].date().strftime("%d-%m-%Y"),
                     'value':v['id'],
                    'status_name': v['last_status__name']
                }
                for v in vacancies
            ]

            j = json.dumps(result)
            return HttpResponse(j, content_type='application/json')



class PhotoDeleteAjax(View):
    '''
        Удаление фото со страницы кандидата
    '''
    def get(self, request):
        if request.is_ajax:
            try:
                id = request.GET['applicant_id']
                applicant = Applicant.objects.get(pk=id)
                applicant.photo = '/media/default.gif'
                applicant.save()
                result = json.dumps(['200'])
            except Exception, e:
                result = json.dumps(['500', e.message])
        else:
            result = json.dumps(['500', 'Is not JSON'])

        return HttpResponse(result, content_type='application/json')

class PhoneDeleteAjax(View):
    '''
        Удаление номера телефона со страницы кандидата
    '''
    def get(self, request):
        if request.is_ajax:
            try:
                id = request.GET['phone_id']
                Phone.objects.get(pk=id).delete()
                result = json.dumps(['200'])
            except Exception, e:
                result = json.dumps(['500', e.message])
        else:
            result = json.dumps(['500', 'Is not JSON'])

        return HttpResponse(result, content_type='application/json')


class EducationDeleteAjax(View):
    '''
        Удаление записи об образовании со страницы кандидата
    '''
    def get(self, request):
        if request.is_ajax:
            try:
                id = request.GET['edu_id']
                ApplicantEducation.objects.get(pk=id).delete()
                result = json.dumps(['200'])
            except Exception, e:
                result = json.dumps(['500', e.message])
        else:
            result = json.dumps(['500', 'Is not JSON'])

        return HttpResponse(result, content_type='application/json')

class PortfolioDeleteAjax(View):
    '''
        Удаление портфолио
    '''
    def get(self, request):
        if request.is_ajax:
            try:
                id = request.GET['portfolio_id']
                Portfolio.objects.get(pk=id).delete()
                result = json.dumps(['200'])
            except Exception, e:
                result = json.dumps(['500', e.message])
        else:
            result = json.dumps(['500', 'Is not JSON'])

        return HttpResponse(result, content_type='application/json')

class ResumeDeleteAjax(View):
    '''
        Удаление резюме
    '''
    def get(self, request):
        if request.is_ajax:
            try:
                id = request.GET['resume_id']
                Resume.objects.get(pk=id).delete()
                result = json.dumps(['200'])
            except Exception, e:
                result = json.dumps(['500', e.message])
        else:
            result = json.dumps(['500', 'Is not JSON'])

        return HttpResponse(result, content_type='application/json')

class ChangePhoneAjax(View):
    '''
        Изменение номера телефона
    '''
    def get(self, request):
        if request.is_ajax:
            try:
                id = request.GET['id']
                phone = request.GET['phone']
                phone_obj = Phone.objects.get(pk=id)


                chars_to_remove = ['(', ')', ' ', '‒'.decode('unicode_escape').encode('ascii','ignore'), '-']
                phone = self.replaceLetters(phone, chars_to_remove)

                print id, phone, phone_obj
                phone_obj.phone = phone
                phone_obj.save()
                print id, phone, phone_obj
                result = json.dumps(['200'])
            except Exception, e:
                result = json.dumps(['500', e.message])
        else:
            result = json.dumps(['500', 'Is not JSON'])

        return HttpResponse(result, content_type='application/json')

    # удаление ненужных символов
    def replaceLetters(self, word, letters):
        word = word.encode('utf8')
        result = ''
        for letter in word:
            if letter not in letters:
                result += letter.decode('unicode_escape').encode('ascii','ignore')
        return result

class PaginatorView(View):
    '''
        разбивка результата поиска по страницам
    '''
    def paginator(self, request, obj_list):
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation
        args = {}
        args['form_search'] = CandidateSearchForm(request.GET)
        p = Paginator(obj_list, 10, request=request)
        applicants = p.page(page)

        args['applicants'] = applicants
        try:
            args['total_applicants_count'] = obj_list.count()
        except:
            args['total_applicants_count'] = len(obj_list)
        rc = RequestContext(request, args)
        print 'RC', rc
        return render_to_response(self.template, rc)


class ApplicantSearchView(PaginatorView):
    '''
        Расширенный поиск кандидатов
    '''
    template = 'applicants/applicant_search.html'

    @method_decorator(login_required)
    def get(self, request):
        applicant_vacancy_list = []

        # выбираем случайных кандидатов, если нет данных в запросе
        if not request.GET:
            applicant_vacancy_list = Applicant.objects.all()\
                                        .values('id', 'last_name',
                                                'first_name', 'middle_name',
                                                'email', 'photo', 'birthday').order_by('?')[:10]
            # получение телефонов кандидата
            for applicant in applicant_vacancy_list:
                phones = Phone.objects.filter(applicant=Applicant.objects.get(pk=applicant['id'])).values('phone')
                applicant['phones'] = phones

        else:
            req = request.GET.copy()


            position = req['position']
            age_add = req.get('age_add', False)
            salary_add = req.get('salary_add', False)
            employee = req.get('employee', False)
            phone = req.get('phone', False)

            # кандидаты из резерва
            reserve = request.GET.get('reserve' or None)

            applicant_fields = [
                'first_name',
                'last_name',
                'middle_name',
                'email',
                'sex'
            ]

            if phone:
                # удаление ненужных символов
                chars_to_remove = ['(', ')', ' ', '‒'.decode('unicode_escape').encode('ascii','ignore'), '-']
                phone = self.replaceLetters(phone, chars_to_remove)
                applicant_obj = Phone.objects.filter(phone=phone).values('applicant')

                applicant_vacancy_list = Applicant.objects.filter(id=applicant_obj[0]['applicant'])\
                                            .values('id', 'last_name',
                                                    'first_name', 'middle_name',
                                                    'email', 'photo', 'birthday')

            # если установлена галочка резерв
            elif reserve:
                # получаем объект статуса
                reserve_object = ApplicantVacancyStatus.objects.get(name__contains='Резерв')
                # получаем объекты вакансий кандидатов
                applicant_vacancy = ApplicantVacancy.objects.all()


                # перебираем
                for av in applicant_vacancy:
                    try:
                        s = CurrentApplicantVacancyStatus.objects.filter(applicant_vacancy=av)
                        # получаем последний статус
                        last_status = s[s.count()-1]
                        status = last_status.applicant_vacancy_status
                        if status == reserve_object:
                            applicant_vacancy_list.append(last_status.applicant_vacancy.applicant)
                    except:
                        pass
            else:
                query_list = {}
                # ключи для поиска в Applicants
                query_applicant_list = {}
                for field in applicant_fields:
                    if req[field]:
                        query_applicant_list[field + '__contains'] = req[field]
                        query_list['applicant__' + field + '__contains'] = req[field]

                # добавляем минимальную и максимальную дату рождения кандидата
                if age_add:
                    today = datetime.date.today()
                    age_min = int(req['age_start'])
                    age_max = int(req['age_end'])


                    date_start = datetime.date(today.year - age_max - 1, today.month, today.day)
                    date_end = datetime.date(today.year - age_min - 1, today.month, today.day)

                    query_list['applicant__birthday__gte'] = query_applicant_list['birthday__gte'] = date_start
                    query_list['applicant__birthday__lte'] = query_applicant_list['birthday__lte'] = date_end

                applicant_vacancy_list = []
                # ищем кандидатов по выбранной должности
                if position:
                    query_list['vacancy__position'] = position

                    if salary_add:
                        salary_start = int(req['salary_start'].replace(' ', ''))
                        salary_end = int(req['salary_end'].replace(' ', ''))
                        # если минимальная и максимальная запрашиваемые суммы одинаковы, то вычисляем +-5% от заданной суммы.
                        if salary_start == salary_end:
                            range_salary = float(salary_start * 5) / 100.0
                            salary_start = float(salary_start) - range_salary
                            salary_end = float(salary_end + range_salary)

                        query_list['salary__gte'] = salary_start
                        query_list['salary__lte'] = salary_end


                    if employee:
                        del query_list['salary__gte']
                        del query_list['salary__lte']
                        # получаем объект статуса
                        reserve_object = ApplicantVacancyStatus.objects.get(name__contains='Принят на работу')
                        # получаем объекты вакансий кандидатов
                        applicant_vacancy = ApplicantVacancy.objects.filter(**query_list)

                        # перебираем
                        for av in applicant_vacancy:
                            try:
                                s = CurrentApplicantVacancyStatus.objects.filter(applicant_vacancy=av)
                                # получаем последний статус
                                last_status = s[s.count()-1]
                                status = last_status.applicant_vacancy_status
                                if status == reserve_object:
                                    applicant_vacancy_list.append(last_status.applicant_vacancy.applicant)
                            except:
                                pass
                    else:
                        buf_applicant_vacancy = ApplicantVacancy.objects.filter(**query_list)\
                            .order_by('salary')\
                            .values('applicant', 'applicant__last_name',
                                'applicant__first_name', 'applicant__middle_name',
                                'applicant__email', 'applicant__photo', 'salary', 'applicant__birthday')

                        applicant_vacancy_list = []
                        for av in buf_applicant_vacancy:
                            applicant_vacancy_list.append({
                                'id': av['applicant'],
                                'last_name': av['applicant__last_name'],
                                'first_name': av['applicant__first_name'],
                                'middle_name': av['applicant__middle_name'],
                                'email': av['applicant__email'],
                                'photo': av['applicant__photo'],
                                'birthday': av['applicant__birthday']
                            })

                else:
                    applicant_vacancy_list = Applicant.objects.filter(**query_applicant_list)\
                                            .values('id', 'last_name',
                                                    'first_name', 'middle_name',
                                                    'email', 'photo', 'birthday')


        # получение телефонов  и последнего статуса кандидата
        for applicant in applicant_vacancy_list:
            print applicant
            try:
                applicant_object = Applicant.objects.get(pk=applicant['id'])
            except:
                try:
                    applicant_object = Applicant.objects.get(pk=applicant['applicant'])
                except:
                    applicant_object = Applicant.objects.get(pk=applicant.id)
            phones = Phone.objects.filter(applicant=applicant_object).values('phone')
            try:
                applicant['phones'] = phones
            except:
                applicant.phones = phones



            try:
                status = CurrentApplicantVacancyStatus.objects.filter(applicant_vacancy__applicant=applicant_object).last()
            except:
                status = None

            try:
                applicant['status'] = status
            except:
                applicant.status = status

        return self.render(request, applicant_vacancy_list)

    # удаление ненужных символов
    def replaceLetters(self, word, letters):
        word = word.encode('utf8')
        result = ''
        for letter in word:
            if letter not in letters:
                result += letter.decode('unicode_escape').encode('ascii','ignore')
        return result

    def render(self, request, result_list, total_count=0):
        return self.paginator(request, result_list)



# вывод информации о кандидате
class ApplicantView(View, SavingModels):
    template = 'applicants/applicant_view.html'

    @method_decorator(login_required)
    def get(self, request, applicant_id):

        applicant = get_object_or_404(Applicant, id=applicant_id)

        applicant_instance = {'instance': applicant}
        args = self.addForms(applicant_instance)

        args['vacancies'] = applicant.applicantvacancy_set.all()

        args['educations'] = applicant.applicanteducation_set.all()
        args['phones'] = Phone.objects.filter(applicant=applicant).values('id', 'phone')
        args['resume'] = Resume.objects.filter(applicant=applicant).values('id', 'resume_file', 'date_upload')
        args['portfolio'] = Portfolio.objects.filter(applicant=applicant).values('portfolio_file', 'date_upload')
        args['applicant_id'] = applicant_id

        try:
            # последний статус кандидата
            last_status = CurrentApplicantVacancyStatus.objects.filter(applicant_vacancy__applicant__id=applicant_id).last()
            print applicant_id, CurrentApplicantVacancyStatus.objects.filter(id=applicant_id), last_status
            args['last_status'] = '%s - %s' % (last_status.applicant_vacancy_status.name, last_status.applicant_vacancy.vacancy.position.name)
        except Exception, e:
            print e.message
            args['last_status'] = None

        args['history_action'] = HistoryChangeApplicantInfo.objects.filter(applicant=applicant)
        args['applicant_vacancy_status'] = ApplicantVacancyStatus.objects.all()

        rc = RequestContext(request, args)
        return render_to_response(self.template, rc)

    # обновление информации
    @method_decorator(login_required)
    def post(self, request, applicant_id):
        if request.is_ajax:
            instance = get_object_or_404(Applicant, id=applicant_id)
            result = self.savingApplicantForm(request, 'Изменён', {'instance': instance})

            if result:
                json_res = json.dumps(['200',result])
            else:
                json_res = json.dumps(['500',result])
            #return HttpResponseRedirect(reverse('applicants:applicant_view', kwargs={'applicant_id':int(applicant_id)}))
            #url = reverse('applicant_view', kwargs={'applicant_id': int(applicant_id)})
            #return redirect('applicants:applicant_view', applicant_id=int(applicant_id))
        else:
            json_res = json.dumps(['200'])


        return HttpResponse(json_res, 'application/json')



class ApplicantVacancyStatusAjax(View):
    '''
        Выборка статусов вакансий для
        определённого кандидата
    '''
    def get(self, request):
        if request.is_ajax:
            request = request.GET

            result_obj = CurrentApplicantVacancyStatus.objects.filter(applicant_vacancy=request['applicant_vacancy']).values('date', 'applicant_vacancy_status__name', 'note')
            result = [
                {
                    'date': i['date'].strftime('%d-%m-%Y'),
                    'status': i['applicant_vacancy_status__name'],
                    'note': i['note']
                }
                for i in result_obj
            ]

            if result:
                json_res = json.dumps(['200', result])
            else:
                json_res = json.dumps(['200'])
        else:
            json_res = json.dumps(['500'])

        return HttpResponse(json_res, content_type='application/text')

    def post(self, request):
        '''
            Добавление статуса кандидидату
        '''
        if request.is_ajax:
            request = request.POST
            user = User.objects.get(pk=request['user_id'])

            try:
                applicant_vacancy_status = ApplicantVacancyStatus.objects.get(pk=request['status'])
            except:
                applicant_vacancy_status = ApplicantVacancyStatus(name=request['status'], author=user)
                applicant_vacancy_status.save()

            obj = CurrentApplicantVacancyStatus(
                applicant_vacancy= ApplicantVacancy.objects.get(pk=request['applicant_vacancy']),
                applicant_vacancy_status = applicant_vacancy_status,
                author = user,
                note = bleach.clean(request['note'])
            )
            obj.save()

            js = [obj.date.strftime('%d-%m-%Y')]
            json_res = json.dumps(['200', js])
        else:
            json_res = json.dumps(['500'])

        return HttpResponse(json_res, content_type='application/text')

class PositionSourceGetAjax(View):
    '''
        Получение всех истоников и всех должностей
    '''
    def get(self, request):
        try:
            positions = Position.objects.all().values('id', 'name')
            sources = SourceInformation.objects.all().values('id', 'source')

            result = json.dumps(['200', {'positions':positions, 'sources':[{'id': s['id'], 'name':s['source']} for s in sources]}])
            return HttpResponse(result, 'application/json')
        except Exception, e:
            result = json.dumps(['500', e.message])
            return HttpResponse(result, 'application/text')
