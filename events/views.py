#-*- coding: utf8 -*-
import datetime
import json
import pytz
from collections import OrderedDict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, render_to_response
from django.views.generic import View
from applicants.models import Applicant, Phone
from vacancies.forms import ApplicantVacancyEventForm
from vacancies.models import ApplicantVacancy, Vacancy
from .models import ApplicantVacancyEvent,Event
from django.template import RequestContext
from utils.functions import fromLocaltoUTC,fromUTCtoLocal
from utils.sending_email import EmailSender


from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class EventsCalendar(View):
    template = 'events/calendar.html'
    @method_decorator(login_required)
    def get(self,request):
        c = RequestContext(request)
        try:
            if request.COOKIES['app_vacancy_id']:
                events = Event.objects.all()
                c = RequestContext(request, {'events':events})
        except:
            pass
        return render_to_response(self.template,c)




class EventsView(View):
    template = 'events/events_view.html'
    @method_decorator(login_required)
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
                                                 'author__username','description','id')

    response = [
        {
            'event':event['event__name'],
            'start':str(event['start'].strftime('%d-%m-%Y %H:%M')),
            'end': str(event['end'].strftime('%d-%m-%Y %H:%M')),
            'author':event['author__username'],
            'description':event['description'],
            'id': event['id']

        }
        for event in events
    ]

    response = json.dumps(response)
    return HttpResponse(response,content_type='application/json')


def add_event_comment_ajax(request):
    app_vacancy_event = ApplicantVacancyEvent.objects.get(applicant_vacancy=request.POST['event_id'])
    app_vacancy_event.description = request.POST['event_description']
    response = []
    try:
        app_vacancy_event.save()
        return JsonResponse(data={},status='200')
    except:

        return JsonResponse(data={},status='400')



def get_events_ajax(request):
    if request.is_ajax:
        result = []
        events = ApplicantVacancyEvent.objects.all()
        for event in events:
            #создаём массив с телефонами в виде строк для передачи в full-calendar
            phones = []
            phones_queryset = list(Phone.objects.filter(applicant = event.applicant_vacancy.applicant))
            for phone in phones_queryset:
                phones.append(str(phone))

            #ссылка на страницу кандидата
            profile_link = '/applicants/view/' + str(event.applicant_vacancy.applicant.id) + '/'
            result.append({'title':event.event.name,
                           'start':fromUTCtoLocal(event.start).isoformat(),
                           'end':fromUTCtoLocal(event.end).isoformat(),
                           'id': event.id,
                           'profile_link':profile_link,
                           'name':event.applicant_vacancy.applicant.getFullName(),
                           'phones':phones,
                           'email': event.applicant_vacancy.applicant.email,
                           'author': event.author.username,
                           'color': event.event.color
                           })


        response = json.dumps(result)
        return HttpResponse(response,content_type='application/json')



def add_event(request):
    if request.is_ajax:
        app_vacancy_id = request.POST['app_vacancy_id']
        applicant_vacancy = ApplicantVacancy.objects.get(
            id=app_vacancy_id)
        event = request.POST["event_type"]

        start = datetime.datetime.strptime(request.POST['start'],
                                           "%Y-%m-%dT%H:%M:%S")

        end = datetime.datetime.strptime(request.POST['end'],"%Y-%m-%dT%H:%M:%S")

        form = ApplicantVacancyEventForm({
            'event':event,'start':start,'end':end})


        if form.is_valid():
            form.instance.applicant_vacancy = applicant_vacancy
            form.instance.author = request.user

            form.save()
            return HttpResponse ("200")

        return HttpResponse("400")






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


def httpresponsejson(code, message):
    #result = json.dumps([code, message])
    return JsonResponse({'code': code, 'messages': message})
    #return HttpResponse(result, content_type='application/json')

# send email
def send_message_ajax(request):
    if request.is_ajax():
        # send email
        method = request.POST
        try:
            message = method['message']
            recipients = [method['email']]
            title = method['title']
        except Exception, e:
            return httpresponsejson('500', 'Преданы не все параметры (сообщение, тема, кому отправить)')

        sender = EmailSender()
        result = sender.send(message, recipients, title)
        if result:
            return httpresponsejson('200', 'Success')
        return httpresponsejson('500', 'Error send')


