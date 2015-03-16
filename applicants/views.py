#-*- coding:utf8 -*-
from django.shortcuts import render, render_to_response
from django.views.generic import View
from django.template import RequestContext

from django.forms.formsets import formset_factory
from forms import ApplicantForm, CandidateSearchForm #, ApplicantEducationForm
from models import Education, Major, SourceInformation, Applicant, Resume, Portfolio

import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

import datetime

# Create your views here.

# Добавление кандидата
class ApplicantAddView(View):
    template = 'applicants/applicant_add.html'
    def get(self, request):
        form = ApplicantForm()
        #edu_form = formset_factory(ApplicantEducationForm, extra=5)


        edu = Education.objects.all()
        major = Major.objects.all()
        source = SourceInformation.objects.all()

        args = {}
        args['applicant_form'] = form
        #args['edu_form'] = edu_form

        args['edu'] = edu
        args['majors'] = major
        args['sources'] = source
        rc = RequestContext(request, args)
        return render_to_response(self.template, rc)

    def post(self, request):
        req = request.POST
        sf = SavingFiles()

# сохранение данных в таблицу Applicant
        applicant_form = ApplicantForm(request.POST, request.FILES)
        new_applicant = applicant_form.save()
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



        return render('fff')

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

class CandidateSearchView(View):
    template = 'applicants/candidate_search.html'
    def get(self, request):
        args = {}
        args['form_search'] = CandidateSearchForm
        rc = RequestContext(request, args)
        return render_to_response(self.template, rc)