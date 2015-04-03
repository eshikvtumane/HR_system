#-*- coding: utf8 -*-
from django.shortcuts import render,render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.template import RequestContext
from forms import AddVacancyForm, EditVacancyForm, SearchVacancyForm
from events.models import ApplicantVacancyEvent
from .models import Department, Head, Vacancy, Position, VacancyStatus, VacancyStatusHistory
from events.models import ApplicantVacancyEvent
import json
from django.core import serializers
import datetime
import pytz
import json




####HELPER FUNCTIONS######################
def fromUTCtoLocal(time):

    now_utc = time
    local_tz = pytz.timezone("Asia/Vladivostok")
    local_time = now_utc.astimezone(local_tz)
    return local_time


def fromLocaltoUTC(time):
    now_local = time
    local_tz = pytz.timezone("Asia/Vladivostok")
    now_local = now_local.replace(tzinfo=local_tz)
    utc_tz= pytz.timezone("UTC")
    utc_time = now_local.astimezone(utc_tz)
    return utc_time
##########################################



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
            vacancy_form = AddVacancyForm(post_data)
            if vacancy_form.is_valid():
                    vacancy_form.instance.author = request.user
                    vacancy_form.save()
                    vacancy_id = vacancy_form.instance.id
                    response = json.dumps([{'vacancy_id':vacancy_id}])
                    return HttpResponse(response,content_type='application/json')
            else:

                    return HttpResponse("400")


class VacancyView(View):
    template = 'vacancies/vacancy_view.html'
    def get(self,request,id):
        vacancy = Vacancy.objects.get(pk=id)
        head = vacancy.head
        c = RequestContext(request,{ 'vacancy':vacancy,'head':head},)
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
        vacancy_form = SearchVacancyForm()
        c = RequestContext(request,{'vacancy_form':vacancy_form})
        return render_to_response(self.template,c)






###AJAX REQUESTS#################
def get_heads_ajax(request):
    if request.is_ajax:
        department_id = int(request.GET['department'])
        heads = list(Head.objects.filter(department=department_id).values('id','name'))
        heads = json.dumps(heads)
        return HttpResponse(heads,content_type='application/json')


def get_events_ajax(request):
    if request.is_ajax:
        result = []
        events = ApplicantVacancyEvent.objects.all()
        for event in events:
            result.append({'title':event.event.name,
                           'start':fromUTCtoLocal(event.start).isoformat(),
                           'end':fromUTCtoLocal(event.end).isoformat(),
                           'id': event.id})

        response = json.dumps(result)
        return HttpResponse(response,content_type='application/json')


def update_event_ajax(request):
    if request.is_ajax():
        event =  ApplicantVacancyEvent.objects.get(id=request.POST["id"])
        new_start =datetime.datetime.strptime(request.POST[
                                                               'start'],
                                           "%Y-%m-%dT%H:%M:%S")

        new_end = datetime.datetime.strptime(request.POST[
                                                               'end'],
                                           "%Y-%m-%dT%H:%M:%S")

        event.start = new_start
        event.end = new_end
        event.save()


def save_event_ajax(request):
    if request.is_ajax():
        new_start = datetime.datetime.strptime(request.POST['start'], "%d/%m/%Y %H:%M")

        new_end = datetime.datetime.strptime(request.POST['end'], "%d/%m/%Y %H:%M")
        event =  ApplicantVacancyEvent.objects.get(id=request.POST["id"])
        try:
            event.start = new_start
            event.end = new_end
            event.save()
            return HttpResponse("200")
        except:
            return HttpResponse("400")




