#-*- coding:utf8 -*-
from django.shortcuts import render, render_to_response, get_object_or_404
from django.views.generic import View
from django.template import RequestContext
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.forms.formsets import formset_factory
from forms import ApplicantForm, CandidateSearchForm, ApplicantEducationForm, VacancyAddForm
from models import Education, Major, SourceInformation, Applicant, Resume, Portfolio, Position, Phone, ApplicantEducation, HistoryChangeApplicantInfo
from vacancies.models import Vacancy, ApplicantVacancy

import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

import json
from django.core import serializers


import datetime

# Create your views here.

class SavingModels():

    def sourceCreate(self, source):
        try:
            convert_id = int(source)
            return convert_id
        except:
            source_obj = SourceInformation(source=source)
            source_obj.save()
            return source_obj.id

    def createMajor(self, major):
        try:
            convert_id = int(major)
            return convert_id
        except:
            major_obj = Major(source=major)
            major_obj.save()
            return major_obj.id

    def savingPhone(self, phones, user):
        if phones:
            phone_obj = [Phone(applicant=user, phone=p) for p in phones if p != '']
            Phone.objects.bulk_create(phone_obj)
        return

    def savingVacancies(self, json_vacancies, user):
        try:
            vacancies = json.loads(json_vacancies)
            vacancy_obj = []

            for k, v in enumerate(vacancies):
                vacancies[v]['vacancy'] = Vacancy(vacancies[v]['vacancy'])
                vacancies[v]['applicant'] = user
                vacancy_obj.append(ApplicantVacancy(**vacancies[v]))

            ApplicantVacancy.objects.bulk_create(vacancy_obj)
            return
        except:
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

    def addForms(self, applicant_instance={}):
        args = {}
        form = ApplicantForm(**applicant_instance)
        edu_form = ApplicantEducationForm()
        vacancy_form = VacancyAddForm()
        positions = Position.objects.all()

        args['applicant_form'] = form
        args['edu_form'] = edu_form
        args['vacancy_form'] = vacancy_form
        args['positions'] = positions

        return args

    def savingApplicantForm(self, request, applicant_instance={}):
        try:
            req = request.POST
            # создание объекта класса сохранения файлов
            sf = SavingFiles()

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

            print applicant_instance
            applicant_form = ApplicantForm(request.POST, request.FILES, **applicant_instance)
            new_applicant = applicant_form.save()

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

            return new_applicant.id
        except:
            return False




# Добавление кандидата
class ApplicantAddView(View, SavingModels):
    template = 'applicants/applicant_add.html'
    def get(self, request):
        args = self.addForms()

        rc = RequestContext(request, args)
        return render_to_response(self.template, rc)

    def post(self, request):
        if request.is_ajax:
            result = self.savingApplicantForm(request)
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


class CandidateSearchView(View):
    template = 'applicants/candidate_search.html'
    def get(self, request):
        args = {}
        args['form_search'] = CandidateSearchForm
        applicants_list = Applicant.objects.all().values('id', 'first_name', 'last_name', 'middle_name', 'photo', 'email')
        paginator = Paginator(applicants_list, 10)

        page = request.GET.get('page')
        try:
            applicants = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            applicants = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            applicants = paginator.page(paginator.num_pages)


        args['applicants'] = applicants
        rc = RequestContext(request, args)
        return render_to_response(self.template, rc)

# вывод информации о кандидате
class ApplicantView(View, SavingModels):
    template = 'applicants/applicant_view.html'
    def get(self, request, applicant_id):

        applicant = get_object_or_404(Applicant, id=applicant_id)
        applicant_instance = {'instance': applicant}
        args = self.addForms(applicant_instance)

        vacancies = applicant.applicantvacancy_set.all()
        educations = applicant.applicanteducation_set.all()

        phones = Phone.objects.filter(applicant=applicant).values('phone')
        resume = Resume.objects.filter(applicant=applicant).values('resume_file', 'date_upload')
        portfolio = Portfolio.objects.filter(applicant=applicant).values('portfolio_file', 'date_upload')

        args['vacancies'] = vacancies
        args['educations'] = educations
        args['phones'] = phones
        args['resume'] = resume
        args['portfolio'] = portfolio
        args['applicant_id'] = applicant_id

        rc = RequestContext(request, args)
        return render_to_response(self.template, rc)

    # обновление информации
    def post(self, request, applicant_id):
        if request.is_ajax:
            instance = get_object_or_404(Applicant, id=applicant_id)
            result = self.savingApplicantForm(request, {'instance': instance})

            # добавление изменения в историю
            HistoryChangeApplicantInfo.objects.create(user=request.user, )

            json_res = json.dumps(['200',result])
        else:
            json_res = json.dumps(['200'])

        return HttpResponse(json_res, 'application/json')