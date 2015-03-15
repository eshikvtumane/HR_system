#-*- coding:utf8 -*-
from django.shortcuts import render, render_to_response
from django.views.generic import View
from django.template import RequestContext
from django.http import HttpResponse

from django.forms.formsets import formset_factory
from forms import ApplicantForm, CandidateSearchForm, ApplicantEducationForm, VacancyAddForm
from models import Education, Major, SourceInformation, Applicant, Resume, Portfolio, Position
from vacancies.models import Vacancy

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

    def saveApplicant(self, request):
        print 'w 0'
        attrs = request.POST
        print 'w 0.0.0'
        #photo = self.saveFile(request.FILES['photo'], dir='photo_applicants')
        print 'w 0.0'
        print attrs['source']
        print SourceInformation.objects.get(pk=attrs['source'])
        d = {
            'first_name': attrs['first_name'],
            'last_name': attrs['last_name'],
            'middle_name': attrs['middle_name'],
            'birthday': attrs['birthday'],
            #'photo': photo,
            'city': attrs['city'],
            'street': attrs['street'],
            'building': attrs['building'],
            'email': attrs['email'],
            'skype': attrs['skype'],
            'vk': attrs['vk'],
            'fb': attrs['fb'],
            'icq': int(attrs['icq']),
            'source': SourceInformation.objects.get(pk=attrs['source'])
        }
        print 'w 1'
        app_obj = Applicant(**d)
        app_obj.save()
        print 'w 2'
        '''try:

        except:
            print 'sdfdsfsdfdsfsdfsdfsfdddddddddddddddddd'
            '''
        return  app_obj

    def saveFile(self, file, dir='', path=settings.MEDIA_URL):
        return self.__save(file, dir, path, '')

    def saveFiles(self, files, dir='', path=settings.MEDIA_URL, filename=''):
        arr_path = []
        for f in files:
            arr_path.append(self.__save(f, dir, path, filename))
        return arr_path

    def __save(self, f,  dir, path, filename):
        original_name, file_extension = os.path.splitext(f.name)
        print 'p 1'
        filename = filename + '-' + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + file_extension
        print 'p 2'
        save_path = default_storage.save(os.path.join(dir, filename), ContentFile(f.read()))
        file_url = os.path.join(path, save_path)
        print 'p 3'
        return file_url



# Добавление кандидата
class ApplicantAddView(View, SavingModels):
    template = 'applicant_add.html'
    def get(self, request):
        form = ApplicantForm()
        edu_form = ApplicantEducationForm()
        vacancy_form = VacancyAddForm


        #edu = Education.objects.all()
        positions = Position.objects.all()
        source = SourceInformation.objects.all()

        args = {}
        args['applicant_form'] = form
        args['edu_form'] = edu_form
        args['vacancy_form'] = vacancy_form

        #args['edu'] = edu
        args['positions'] = positions
        rc = RequestContext(request, args)
        return render_to_response(self.template, rc)

    def post(self, request):
        req = request.POST
        sf = SavingFiles()

        req['birthday'] = datetime.datetime.strptime(req['birthday'], "%d-%m-%Y").date()
        print req['birthday'], req['source']
# сохранение данных в таблицу Applicant
        source_id = self.sourceCreate(req['source'])
        request.POST['source'] = source_id
        print source_id, req['source']

        if req['icq']:
            req['icq'] = int(req['icq'])
        else:
            req['icq'] = None

        applicant_form = ApplicantForm(request.POST, request.FILES)

        new_applicant = applicant_form.save()

        #new_applicant = self.saveApplicant(request)
        full_name = new_applicant.getFullName()

        resume = sf.saveFiles(request.FILES.getlist('resume[]'), dir='resume', filename=full_name) #sf.saveFile(request.FILES.get('photo'), 'photo_applicants')
        portfolio = sf.saveFiles(request.FILES.getlist('portfolio[]'), dir='portfolio', filename=full_name)

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



        return HttpResponse('200', 'text/plain')

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
    template = 'candidate_search.html'
    def get(self, request):
        args = {}
        args['form_search'] = CandidateSearchForm
        rc = RequestContext(request, args)
        return render_to_response(self.template, rc)