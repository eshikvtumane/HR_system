#-*- coding: utf8 -*-
import datetime
import json
import pytz
from collections import OrderedDict
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.views.generic import View
from applicants.models import Applicant
from vacancies.forms import ApplicantVacancyEventForm
from vacancies.models import ApplicantVacancy, Vacancy
from .models import ApplicantVacancyEvent
from django.template import RequestContext



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






class EventsView(View):
    template = 'events/events_view.html'
    def get(self,request,applicant_id):
        applicant = Applicant.objects.get(id = applicant_id)
        app_vacancies = ApplicantVacancy.objects.filter(applicant = applicant )
        c = RequestContext(request,{"app_vacancies":app_vacancies})
        return render_to_response(self.template, c)


class EventsAdd(View):
     def post(self,request,applicant_id):
        if request.is_ajax:
            vacancy_id = request.POST['vacancy_id']
            applicant = Applicant.objects.get(id=applicant_id )
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
            return HttpResponse("400")




####ajax functions###############
def get_vacancy_events_ajax(request):
    app_vacancy_id = request.GET["app_vacancy_id"]
    events = ApplicantVacancyEvent.objects.filter(
        applicant_vacancy=app_vacancy_id).values('event__name','start','end',
                                                 'author__username','happened','description','id')

    response = [
        {
            'event':event['event__name'],
            'start':str(event['start'].strftime('%d-%m-%Y %H:%M')),
            'end': str(event['end'].strftime('%d-%m-%Y %H:%M')),
            'author':event['author__username'],
            'happened':event['happened'],
            'description':event['description'],
            'id': event['id']

        }
        for event in events
    ]

    response = json.dumps(response)
    return HttpResponse(response,content_type='application/json')


def change_event_status_ajax(request):
    app_vacancy_event = ApplicantVacancyEvent.objects.get(applicant_vacancy=request.POST['event_id'])
    app_vacancy_event.happened = True
    app_vacancy_event.description = request.POST['event_description']
    response = []
    try:
        app_vacancy_event.save()
        response.append({'status':'200'})
        return HttpResponse(response,content_type='application/json')
    except:
        response.append({'status':'400'})
    return HttpResponse(response,content_type='application/json')



def get_events_ajax(request):
    if request.is_ajax:
        result = []
        events = ApplicantVacancyEvent.objects.all()
        for event in events:
            profile_link = 'applicants/view/' + str(event.applicant_vacancy.applicant.id) + '/'
            print "Applicant id is " + profile_link
            result.append({'title':event.event.name,
                           'start':fromUTCtoLocal(event.start).isoformat(),
                           'end':fromUTCtoLocal(event.end).isoformat(),
                           'id': event.id,
                           'profile_link':profile_link} )

        response = json.dumps(result)
        return HttpResponse(response,content_type='application/json')


def update_event_ajax(request):
    if request.is_ajax():
        start = request.POST['start']
        end = request.POST['end']
        #обрезаем часть строки с time zone данными
        if len(start)>19:
            start = start[:19]
            end =  end[:19]

        event =  ApplicantVacancyEvent.objects.get(id=request.POST["id"])
        new_start =datetime.datetime.strptime(start,
                                           "%Y-%m-%dT%H:%M:%S")

        new_end = datetime.datetime.strptime(end,
                                           "%Y-%m-%dT%H:%M:%S")
        try:
            event.start = new_start
            event.end = new_end
            event.save()
            return HttpResponse('200')
        except:
            return HttpResponse('400')



def delete_event_ajax(request):
    if request.is_ajax():
        event = ApplicantVacancyEvent.objects.get(id=request.POST["event_id"])
        try:
            event.delete()
            return HttpResponse('200')
        except:
            return  HttpResponse('400')
