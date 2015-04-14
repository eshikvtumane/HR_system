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
    ApplicantVacancyStatus, ApplicantVacancyApplicantVacancyStatus

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
            source_obj = SourceInformation(source=source, author=self.author)
            source_obj.save()
            return source_obj

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
            if phones:
                phone_obj = [Phone(applicant=user, phone=p) for p in phones if p != '']
                Phone.objects.bulk_create(phone_obj)

            return
        except:
            return

    def savingVacancies(self, json_vacancies, user):
        try:
            vacancies = json.loads(json_vacancies)
            vacancy_obj = []

            for k, v in enumerate(vacancies):
                vacancies[v]['vacancy'] = Vacancy(vacancies[v]['vacancy'])
                vacancies[v]['applicant'] = user
                vacancies[v]['source'] = self.sourceCreate(vacancies[v]['source'])
                vacancy_obj.append(ApplicantVacancy(**vacancies[v]))

            ApplicantVacancy.objects.bulk_create(vacancy_obj)
            return
        except Exception, e:
            print e.message
            return

    def savingEducations(self, json_educations, user):
        try:
            educations = json.loads(json_educations)
            edu_obj = []

            for k, v in enumerate(educations):
                educations[v]['education'] = Education.objects.get(pk=educations[v]['education'])
                educations[v]['major'] = Major.objects.get(pk=self.createMajor(educations[v]['major']))
                educations[v]['applicant'] = user
                edu_obj.append(ApplicantEducation(**educations[v]))

            ApplicantEducation.objects.bulk_create(edu_obj)
        except:
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
        try:
            req = request.POST
            self.author = request.user
            # создание объекта класса сохранения файлов
            sf = SavingFiles()

            req['date_created'] = datetime.datetime.now()
            # конвертирование даты в формат, понятный БД
            try:
                req['birthday'] = datetime.datetime.strptime(req['birthday'], "%d-%m-%Y").date()
            except:
                req['birthday'] = datetime.datetime.strptime(req['birthday'], "%Y-%m-%d").date()

            # сохранение данных в таблицу Applicant
            # сохраниение нового источника или получение id существующего источника
            request.POST['source'] = self.sourceCreate(req['source'])

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

            self.savingPhone(req.getlist('phone'), new_applicant)
            self.savingVacancies(req['vacancies'], new_applicant)
            self.savingEducations(req['educations'], new_applicant)

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
        except Exception, e:
            print e.message
            return False




# Добавление кандидата
class ApplicantAddView(View, SavingModels):
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
    '''def saveFile(self, file, dir='', path=settings.MEDIA_URL):
        return self.__save(file, dir, path)'''

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

# выборка вакансий
class VacancySearchAjax(View):
    def get(self, request):
        if request.is_ajax:
            position = request.GET.get('position')
            vacancies = Vacancy.objects.filter(position=position).values('head__name', 'id', 'published_at')
            result = [
                {'head': v['head__name'],
                 'date': v['published_at'].date().strftime("%d-%m-%Y"),
                 'value':v['id']
                }
                for v in vacancies
            ]

            j = json.dumps(result)
            return HttpResponse(j, content_type='application/json')

class PaginatorView(View):
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
        rc = RequestContext(request, args)
        return render_to_response(self.template, rc)


class ApplicantSearchView(PaginatorView):
    template = 'applicants/applicant_search.html'

    @method_decorator(login_required)
    def get(self, request):
        if not request.GET:
            applicant_vacancy_list = Applicant.objects.all()\
                                        .values('id', 'last_name',
                                                'first_name', 'middle_name',
                                                'email', 'photo').reverse()[:10]
        else:
            req = request.GET.copy()


            position = req['position']

            applicant_fields = [
                'first_name',
                'last_name',
                'middle_name',
                'email',
                'sex'
            ]


            query_list = {}
            # ключи для поиска в Applicants
            query_applicant_list = {}
            for field in applicant_fields:
                if req[field]:
                    query_applicant_list[field + '__contains'] = req[field]
                    query_list['applicant__' + field + '__contains'] = req[field]

            if position:
                query_list['vacancy__position'] = position

                salary_start = int(req['salary_start'].replace(' ', ''))
                salary_end   = int(req['salary_end'].replace(' ', ''))
                if salary_start == salary_end:
                    range_salary = float(salary_start * 5) / 100.0
                    salary_start = float(salary_start) - range_salary
                    salary_end = float(salary_end + range_salary)

                query_list['salary__gte'] = salary_start
                query_list['salary__lte'] = salary_end

                applicant_vacancy_list = ApplicantVacancy.objects.filter(**query_list)\
                    .order_by('salary')\
                    .values('applicant', 'applicant__last_name',
                            'applicant__first_name', 'applicant__middle_name',
                            'applicant__email', 'applicant__photo', 'salary')

            else:
                #applicant_list = Applicant.objects.filter(query_applicant_list)
                applicant_vacancy_list = Applicant.objects.filter(**query_applicant_list)\
                                        .values('id', 'last_name',
                                                'first_name', 'middle_name',
                                                'email', 'photo')


        return self.render(request, applicant_vacancy_list)

    def render(self, request, result_list):
        return self.paginator(request, result_list)



# вывод информации о кандидате
class ApplicantView(View, SavingModels):
    template = 'applicants/applicant_view.html'

    @method_decorator(login_required)
    def get(self, request, applicant_id):

        applicant = get_object_or_404(Applicant, id=applicant_id)
        print '=' * 40
        print [a for a in dir(applicant) if 'Age' in a]

        applicant_instance = {'instance': applicant}
        args = self.addForms(applicant_instance)

        args['vacancies'] = applicant.applicantvacancy_set.all()
        args['educations'] = applicant.applicanteducation_set.all()
        args['phones'] = Phone.objects.filter(applicant=applicant).values('phone')
        args['resume'] = Resume.objects.filter(applicant=applicant).values('resume_file', 'date_upload')
        args['portfolio'] = Portfolio.objects.filter(applicant=applicant).values('portfolio_file', 'date_upload')
        args['applicant_id'] = applicant_id

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

            json_res = json.dumps(['200',result])
            #return HttpResponseRedirect(reverse('applicants:applicant_view', kwargs={'applicant_id':int(applicant_id)}))
            #url = reverse('applicant_view', kwargs={'applicant_id': int(applicant_id)})
            #return redirect('applicants:applicant_view', applicant_id=int(applicant_id))
        else:
            json_res = json.dumps(['200'])


        return HttpResponse(json_res, 'application/json')




class ApplicantEventAjax(View):
    def post(self,request,applicant_id):
        if request.is_ajax:
            vacancy_id = request.POST['vacancy_id']
            applicant = Applicant.objects.get(id=applicant_id )
            print "dasdad" + vacancy_id
            vacancy = Vacancy.objects.get(id = vacancy_id)
            applicant_vacancy = ApplicantVacancy.objects.get(
                applicant=applicant,vacancy=vacancy)


            event = request.POST["event"]
            start = datetime.datetime.strptime(request.POST['start'],
                                               "%d/%m/%Y %H:%M")

            end = datetime.datetime.strptime(request.POST['end'], "%d/%m/%Y "
                                                                  "%H:%M")
            form = ApplicantVacancyEventForm({
                'event':event,'start':start,'end':end})

            if form.is_valid():
                form.instance.applicant_vacancy = applicant_vacancy
                form.instance.author = request.user
                form.save()
                return HttpResponse ("200")
            print(form.errors)
            return HttpResponse("400")




class ApplicantVacancyStatusAjax(View):
    def get(self, request):
        if request.is_ajax:
            request = request.GET

            result_obj = ApplicantVacancyApplicantVacancyStatus.objects.filter(applicant_vacancy=request['applicant_vacancy']).values('date', 'applicant_vacancy_status__name', 'note')
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
        if request.is_ajax:
            request = request.POST
            obj = ApplicantVacancyApplicantVacancyStatus(
                applicant_vacancy=ApplicantVacancy.objects.get(pk=request['applicant_vacancy']),
                applicant_vacancy_status = ApplicantVacancyStatus.objects.get(pk=request['status']),
                author = User.objects.get(pk=request['user_id']),
                note = bleach.clean(request['note'])
            )
            obj.save()

            js = [obj.date.strftime('%d-%m-%Y')]
            json_res = json.dumps(['200', js])
        else:
            json_res = json.dumps(['500'])

        return HttpResponse(json_res, content_type='application/text')

