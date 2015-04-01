import datetime
import json
from collections import OrderedDict
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.views.generic import View
from applicants.models import Applicant
from vacancies.forms import ApplicantVacancyEventForm
from vacancies.models import ApplicantVacancy, Vacancy
from .models import ApplicantVacancyEvent
from django.template import RequestContext


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


def get_vacancy_events_ajax(request):
    app_vacancy_id = request.GET["app_vacancy_id"]
    events = ApplicantVacancyEvent.objects.filter(
        applicant_vacancy=app_vacancy_id).values('event__name','start','end',
                                                 'author__username','happened')





    response = [
        {
            'event':event['event__name'],
            'start':str(event['start'].strftime('%d-%m-%Y %H:%M')),
            'end': str(event['end'].strftime('%d-%m-%Y %H:%M')),
            'author':event['author__username'],
            'happened':event['happened']

        }
        for event in events
    ]
    print response
    response = json.dumps(response)
    print response
    return HttpResponse(response,content_type='application/json')






