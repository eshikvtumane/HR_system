#-*- coding: utf8 -*-

import datetime
import pytz
import json
from django.core import serializers
from pure_pagination import Paginator, PageNotAnInteger
from django.shortcuts import render,render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.template import RequestContext
from forms import AddVacancyForm, EditVacancyForm, SearchVacancyForm
from events.models import ApplicantVacancyEvent
from applicants.models import Applicant
from .models import Department, Head, Vacancy, Position, VacancyStatus, VacancyStatusHistory, ApplicantVacancy
from events.models import ApplicantVacancyEvent





class AddVacancy(View):
    template = 'vacancies/vacancy_add.html'
    def get(self,request):
        vacancy_form = AddVacancyForm()
        departments  = Department.objects.all()
        c = RequestContext(request,{'vacancy_form':vacancy_form,
                                    'departments':departments}
                                    )
        return render_to_response(self.template,c)


    def post(self,request):
        if request.is_ajax:
            post_data = request.POST.copy()
            post_data['end_date'] = datetime.datetime.strptime(post_data['end_date'],
                                                     '%d-%m-%Y').date()
            post_data['author'] = request.user
            post_data['last_status'] = VacancyStatus.objects.get(name='Открыта')
            vacancy_form = AddVacancyForm(post_data)
            if vacancy_form.is_valid():
                    vacancy_form.instance.author = request.user
                    vacancy_form.save()
                    VacancyStatusHistory.objects.create(vacancy=vacancy_form.instance)
                    vacancy_id = vacancy_form.instance.id
                    response = json.dumps([{'vacancy_id':vacancy_id}])
                    return HttpResponse(response,content_type='application/json')
            else:

                    return HttpResponse("400")


class VacancyView(View):
    template = 'vacancies/vacancy_view.html'
    def get(self,request,id):
        vacancy = Vacancy.objects.get(pk=id)
        app_vacancies = ApplicantVacancy.objects.filter(vacancy_id = vacancy.id)
        applicants = []
        for app_vacancy in app_vacancies:
            applicants.append(app_vacancy.applicant)
        head = vacancy.head
        c = RequestContext(request,{ 'vacancy':vacancy,'head':head,'applicants':applicants})
        return render_to_response(self.template, c)


class VacancyEdit(View):
    template = 'vacancies/vacancy_edit.html'
    def get(self,request,id):
        vacancy = Vacancy.objects.get(pk=id)
        #Выбираем последнюю запись из таблицы с историей изменения статусов вакансии для выбора последнего присвоенного
        #вакансии статуса для установки дефолтного значения в виджете со статусами
        last_vacancy_status_history = VacancyStatusHistory.objects.filter(vacancy=vacancy).order_by('-id')[0]
        default_vacancy_status = last_vacancy_status_history.status
        vacancy_form = EditVacancyForm(instance=vacancy,initial={'status':default_vacancy_status.id})
        c = RequestContext(request,{ 'vacancy':vacancy,'vacancy_form':vacancy_form})
        return render_to_response(self.template, c)

    def post(self,request,id):
        if request.is_ajax:
            post_data = request.POST.copy()
            post_data['end_date'] = datetime.datetime.strptime(post_data['end_date'],
                                                       '%d-%m-%Y').date()

            vacancy = Vacancy.objects.get(pk=id)
            vacancy.last_status = request.POST['status']
            vacancy_form = EditVacancyForm(post_data,instance=vacancy)
            if vacancy_form.is_valid():
                vacancy_form.save()
                VacancyStatusHistory.objects.create(vacancy=vacancy,status=VacancyStatus.objects.get(pk=request.POST[
                    'status']))
                return HttpResponse("200")
            data = []
            data.append({"status":"400","errors":vacancy_form.errors})
            data = json.dumps(data)
            return HttpResponse(data,content_type="application/json")




class VacancySearch(View):
    template = 'vacancies/vacancy_search.html'
    def get(self,request):

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
                page = 1


        vacancies_list = []
        vacancy_form = SearchVacancyForm()


        if request.GET and len(request.GET) != 1:

            vacancy_form = SearchVacancyForm(request.GET)
            query_list = {}

            result_vacancies = []

            if request.GET['position']:
                query_list['position_id'] = request.GET['position']

            if request.GET['head']:
                query_list['head_id'] = request.GET['head']

            if request.GET['search_start']:
                query_list['published_at__gte'] = datetime.datetime.strptime(request.GET['search_start'],'%d-%m-%Y')

            if request.GET['search_end']:
                query_list['published_at__lte'] =  datetime.datetime.strptime(request.GET['search_end'],'%d-%m-%Y')


            if query_list:
                vacancies = Vacancy.objects.filter(**query_list)
                result_vacancies = list(vacancies)
            else:
                vacancies = []




            if request.GET['status']:
                result_vacancies = []
                if not query_list:
                    vacancies = Vacancy.objects.all()
                for vacancy in vacancies:
                    vacancy_status =  VacancyStatusHistory.objects.filter(vacancy = vacancy).order_by('-id')[0]
                    if vacancy_status.status.id == int(request.GET['status']):
                        result_vacancies.append(vacancy)




            for vacancy in result_vacancies:
                vacancy_status = VacancyStatusHistory.objects.filter(vacancy=vacancy).order_by('-id')[0]
                vacancies_list.append({'vacancy':vacancy,'current_status':vacancy_status.status.name,'status_icon':vacancy_status.status.icon_class})



        else:
            vacancies = Vacancy.objects.all()
            for vacancy in vacancies:
                vacancy_status = VacancyStatusHistory.objects.filter(vacancy=vacancy).order_by('-id')[0]
                vacancies_list.append({'vacancy':vacancy,'current_status':vacancy_status.status.name,'status_icon':vacancy_status.status.icon_class})



        p = Paginator(vacancies_list,2,request=request)
        vacancies_list = p.page(page)
        c = RequestContext(request,{'vacancy_form':vacancy_form,'vacancies_list':vacancies_list})
        return render_to_response(self.template,c)




###AJAX REQUESTS#################
def get_heads_ajax(request):
    if request.is_ajax:
        department_id = int(request.GET['department'])
        heads = list(Head.objects.filter(department=department_id).values('id','name'))
        heads = json.dumps(heads)
        return HttpResponse(heads,content_type='application/json')







