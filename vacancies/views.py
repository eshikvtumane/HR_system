#-*- coding: utf8 -*-
import datetime
import pytz
import json
from django.core import serializers
from pure_pagination import Paginator, PageNotAnInteger
from django.shortcuts import render_to_response,get_object_or_404
from django.http import HttpResponse,JsonResponse
from django.views.generic import View
from django.template import RequestContext
from forms import AddVacancyForm, EditVacancyForm, SearchVacancyForm
from events.models import ApplicantVacancyEvent
from applicants.models import Applicant
from .models import Department, Head, Vacancy, Position, VacancyStatus, VacancyStatusHistory, ApplicantVacancy, \
    Benefit,VacancyBenefit,CurrentApplicantVacancyStatus, Education
from events.models import ApplicantVacancyEvent

from django.db.models.query import QuerySet


class AddVacancy(View):
    template = 'vacancies/vacancy_add.html'
    def get(self,request):

        vacancy_form = AddVacancyForm()
        departments  = Department.objects.all()
        benefits = Benefit.objects.all()
        c = RequestContext(request,{'vacancy_form':vacancy_form,
                                    'departments':departments,
                                    'benefits':benefits}
                                    )
        return render_to_response(self.template,c)


    def post(self,request):
        try:
            post_data = request.POST.copy()
            post_data['end_date'] = datetime.datetime.strptime(post_data['end_date'],
                                                     '%d-%m-%Y').date()
            last_status = VacancyStatus.objects.get_or_create(name=u'Открыта', icon_class='green')

            #возвращается объект вида (object,True/False), поэтому вытаскиваем id объекта(статуса) по первому индексу
            post_data['last_status'] = last_status[0].id
            vacancy_form = AddVacancyForm(post_data)

            #проверяем, каким образом добавлены поля справочников(либо выбраны из базы,либо добавлены в базу динамически
            # через форму добавления вакансии)
            if not post_data['position'].isdigit():
                position = Position(name=post_data['position'], author=request.user)
                position.save()
                post_data['position'] = position.id

            if not post_data['education'].isdigit():
                education = Education(type=post_data['education'], author=request.user)
                education.save()
                post_data['education'] = education.id


            if vacancy_form.is_valid():
                instance = vacancy_form.save(commit=False)
                instance.author = request.user
                instance.last_status = VacancyStatus.objects.get(name='Открыта')
                vacancy_form.save()

                VacancyStatusHistory.objects.create(vacancy=vacancy_form.instance)
                vacancy_id = vacancy_form.instance.id
                #сохраняем льготы
                benefits = post_data.get('benfits' or None)
                if benefits:
                    for benefit in post_data.getlist('benefits'):
                        VacancyBenefit.objects.create(vacancy=Vacancy.objects.get(id=vacancy_id) ,
                                                      benefit=Benefit.objects.get(id=int( benefit)))

                response = {'vacancy_id':vacancy_id}
                return JsonResponse(response, status = 200)
            else:
                return JsonResponse(vacancy_form.errors,status=400)
        except Exception, e:
            return JsonResponse({'errors':'Во время добавления вакансии произошла ошибка!'})



class VacancyView(View):
    template = 'vacancies/vacancy_view.html'
    def get(self,request,id):
        vacancy = get_object_or_404(Vacancy,pk=id)
        app_vacancies = ApplicantVacancy.objects.filter(vacancy_id = vacancy.id)
        applicants = []
        applicant_hired = None

        for app_vacancy in app_vacancies:
            #выбираем последний статус в объектах Applicant-Vacancy по данной вакансии
            try:
                last_status = CurrentApplicantVacancyStatus.objects.filter(applicant_vacancy=app_vacancy).order_by(
                    '-id')[0]

                #добавляем кандидата в массив кандидатов с его текущим статусом по данной вакансии
                applicants.append({'applicant':app_vacancy.applicant,'status':last_status.applicant_vacancy_status.name})

                #если кандидат был принят на работу по данной вакансии, то выводим его данные на страницу
                if last_status.applicant_vacancy_status.name.encode('utf-8').strip() == 'Принят на работу':
                    applicant_hired = app_vacancy.applicant
            except Exception, e:
                print e.message
                applicants.append({'applicant':app_vacancy.applicant,'status':u'Ошибка получения статуса'})



        #руководитель отдела, подавший заявку на вакансию
        head = vacancy.head
        #льготы по данной вакансии
        benefits = []
        vacancy_benefits = VacancyBenefit.objects.filter(vacancy=vacancy)
        for vac_benefit in vacancy_benefits:
            benefits.append(vac_benefit.benefit.name)
        #текущий статус вакансии
        vacancy_status = VacancyStatusHistory.objects.filter(vacancy=vacancy).order_by('-id')[0]
        c = RequestContext(request,{ 'vacancy':vacancy,'head':head,'applicants':applicants,
                                     'applicant_hired':applicant_hired,'current_status':vacancy_status.status.name,
                                     'status_icon':vacancy_status.status.icon_class,'benefits':benefits})
        return render_to_response(self.template, c)


class VacancyEdit(View):
    template = 'vacancies/vacancy_edit.html'
    def get(self,request,id):
        vacancy = get_object_or_404(Vacancy,pk=id)
        #Выбираем последнюю запись из таблицы с историей изменения статусов вакансии для выбора последнего присвоенного
        #вакансии статуса для установки дефолтного значения в виджете со статусами
        last_vacancy_status_history = VacancyStatusHistory.objects.filter(vacancy=vacancy).order_by('-id')[0]
        default_vacancy_status = last_vacancy_status_history.status
        vacancy_form = EditVacancyForm(instance=vacancy,initial={'status':default_vacancy_status.id})
        benefits = Benefit.objects.all()
        vac_benefits = VacancyBenefit.objects.filter(vacancy=vacancy)
        added_benefits = [vac_benefit.benefit.name for vac_benefit in vac_benefits ]
        c = RequestContext(request,{ 'vacancy':vacancy,'vacancy_form':vacancy_form,'benefits':benefits,
                                     'added_benefits':added_benefits})
        return render_to_response(self.template, c)

    def post(self,request,id):
        if request.is_ajax:
            post_data = request.POST.copy()
            post_data['end_date'] = datetime.datetime.strptime(post_data['end_date'],
                                                       '%d-%m-%Y').date()

            vacancy = Vacancy.objects.get(pk=id)
            vacancy.last_status = VacancyStatus.objects.get(pk=request.POST['status'])
            vacancy_form = EditVacancyForm(post_data,instance=vacancy)
            if vacancy_form.is_valid():
                vacancy_form.save()

                benefits = post_data.getlist('benefits' or None)

                if benefits:
                        for benefit in benefits:
                            VacancyBenefit.objects.create(vacancy=Vacancy.objects.get(id=vacancy.id) ,
                                                          benefit=Benefit.objects.get(id=int( benefit)))
                VacancyStatusHistory.objects.create(vacancy=vacancy,status=VacancyStatus.objects.get(pk=request.POST['status']))
                return JsonResponse( {},status=200)
            return JsonResponse({'errors':vacancy_form.errors},status = 400)




class VacancySearch(View):
    template = 'vacancies/vacancy_search.html'

    def get(self,request):

        vacancies_per_page = 10

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



        p = Paginator(vacancies_list,vacancies_per_page,request=request)
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







