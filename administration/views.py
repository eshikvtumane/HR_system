#-*- coding: utf8 -*-
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.generic import View
from django.http import HttpResponse

from applicants.models import Major, SourceInformation
from vacancies.models import ApplicantVacancyStatus

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from datetime import datetime

# Create your views here.
# рендер страницы добавления значений в БД
class ValueAddView(View):
    template = 'administration/name_add.html'
    @method_decorator(login_required)
    def get(self, request):
        args = {}
        rc = RequestContext(request, args)
        return render_to_response(self.template, rc)

# сохранеие значений в БД
class AjaxView(View):
    '''
        Сохранение значений в БД
        model    - модель, куда сохранять значения
        key      - аттрибут в модели
        post_key - ключ, по которому доступны переданные значения в POST с клиента
    '''
    def savingValues(self, request, model, key, post_key):
        files_len = len(request.FILES)

        # если файл существует, то передаём его для записи значений в БД
        if files_len > 0:
            param = request.FILES[post_key]
        # если файл не передали, то передаём список значений
        else:
            req = request.GET
            if request.method == 'POST':
                req = request.POST

            param = req.getlist(post_key)

        return self.__recordDB(param, request.user, model, key)


    # запись переданных значений в БД
    def __recordDB(self, file, user, model, key):
        try:
            # выборка всех записей из БД
            spec_db = model.objects.all().values(key)
            # запись значений из полученной выборки в лист
            obj_list = [m[key].encode('utf-8') for m in spec_db]

            # формирование списка с отсутствующими в БД записями
            result_list = []
            for s in file:
                if s not in obj_list:
                    result_list.append(model(**{key: s, 'author': user}))

            # запись сформированного списка в БД
            model.objects.bulk_create(result_list)
            return HttpResponse('200', content_type='plain/text')
        except Exception, e:
            # возврат сообщения об ошибке
            return HttpResponse(e.message, content_type='plain/text')

# Сохранение специальностей в БД
class MajorSaveView(AjaxView):
    @method_decorator(login_required)
    def post(self, request):
        return self.savingValues(request, Major, 'name', 'speciality[]')

# Сохранение источников в БД
class SourceSaveView(AjaxView):
    @method_decorator(login_required)
    def post(self, request):
        return self.savingValues(request, SourceInformation, 'source', 'source[]')

# Сохранение статусов вакансий в БД
class VacancyStatusSaveView(AjaxView):
    @method_decorator(login_required)
    def post(self, request):
        return self.savingValues(request, ApplicantVacancyStatus, 'name', 'vacancy[]')

