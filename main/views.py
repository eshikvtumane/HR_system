#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.views.generic import View
from django.template import RequestContext
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

import re
from applicants.models import Applicant, Phone
from applicants.views import PaginatorView
from vacancies.models import Vacancy, ApplicantVacancy
from django.db.models import Sum

from main.models import Todo
import json
from django.http import HttpResponse

from datetime import datetime


# Create your views here.
class MainPageView(View):
    template = 'main/main.html'

    @method_decorator(login_required)
    def get(self, request):
        args = {}
        return self.render(request)

    def post(self, request):
        if request.is_ajax:
            args = {}
            record = request.POST['record']
            try:
                task = Todo(task=record, user=request.user)
                task_id = task.save()
                result = {'code': 200, 'result': task.id}
            except Exception, e:
                #result = json.dumps(['500', e.message])
                result = {'code': 500, 'message': e.message}
        return JsonResponse(result, content_type='applicant/json')

    def render(self, request, args={}):
        args['todo'] = Todo.objects.filter(user=request.user)
        applicants = Applicant.objects.all()
        users_count = applicants.count()
        args['users_count'] = users_count

        zero = u'н/д'

        total_age = 0;
        today = datetime.now()
        for a in applicants:
            total_age += today.year - a.birthday.year - ((today.month, today.day) < (a.birthday.month, a.birthday.day))

        args['middle_age'] = self.__calculationMiddleValues(total_age, users_count, zero)

        vacancies = Vacancy.objects.all()
        vacancies_count = vacancies.count()
        total_salary = 0
        for v in vacancies:
            total_salary += v.salary

        args['middle_salary'] = self.__calculationMiddleValues(total_salary, users_count, zero)

        applicant_vacancy = ApplicantVacancy.objects.all()
        vacancies_count = applicant_vacancy.count()
        total_salary = 0
        for v in applicant_vacancy:
            total_salary += v.salary

        args['middle_applicant_salary'] = self.__calculationMiddleValues(total_salary, vacancies_count, zero)

        rc = RequestContext(request, args)
        return render_to_response(self.template, rc)

    def __calculationMiddleValues(self, total, count, zero):
        try:
            return total/count
        except:
            return zero

class TodoDeleteAjax(View):
    '''
        Удаление заметки
    '''
    def get(self, request, record_id):
        id = record_id
        try:
            Todo.objects.get(pk=id).delete()
            result = json.dumps(['200'])
        except Exception, e:
            result = json.dumps(['500', e.message])
        return HttpResponse(result, content_type='applicant/json')

class GlobalSearchView(PaginatorView):
    template = 'applicants/applicant_search.html'#'applicants/applicant_global_search.html'
    @method_decorator(login_required)
    def get(self, request):
        query = request.GET['q']

        # Проверка на существование запроса
        if query:
            # является ли введённая строка email'ом
            if re.match(r'[^@]+@[^@]+\.[^@]+', query):
                applicant = Applicant.objects.filter(email=query)
                return self.render(request, applicant)

            # удаление ненужных символов
            chars_to_remove = ['(', ')', ' ', '‒'.decode('unicode_escape').encode('ascii','ignore'), '-']
            phone = self.replaceLetters(query, chars_to_remove)

            # является ли введённая строка номером телефона
            if re.match(r'\d+', phone):
                # поиск телефона
                try:
                    applicant_id = Phone.objects.get(phone=phone).applicant.id
                    applicant = Applicant.objects.filter(id=applicant_id)
                except:
                    # если нет такого телефона, отпраляем пустой массив
                    applicant = []
                return self.render(request, applicant)

            # поиск по ФИО
            return self.render(request, self.search_name(query))

        return self.render(request, [])

    # удаление ненужных символов
    def replaceLetters(self, word, letters):
        word = word.encode('utf8')
        result = ''
        for letter in word:
            if letter not in letters:
                result += letter.decode('unicode_escape').encode('ascii','ignore')
        return result

    def render(self, request, result):
        return self.paginator(request, result)


    # поиск по ФИО
    def search_name(self, name):
        name = name.split(' ') #self.splitNames(name)
        name_len = len(name)

        # если ФИО полностью введено
        if name_len == 3:
            return Applicant.objects.filter(
                    first_name__icontains = name[0],
                    last_name__icontains = name[1],
                    middle_name__icontains = name[2]
                )
        # если введены фамилия и имя
        if name_len == 2:
            applicant = Applicant.objects.filter(
                    first_name__icontains = name[0],
                    last_name__icontains = name[1]
                )

            if not applicant:
                return Applicant.objects.filter(
                    first_name__icontains = name[1],
                    last_name__icontains = name[0]
                )

            return applicant

        # если введена фамилия
        if name_len == 1:
            return Applicant.objects.filter(
                    first_name__icontains = name[0]
                )

        return []
'''
    def splitNames(self, names):
        names = names.split(' ')

        for name in names:
            name = name.title()

        return names'''


