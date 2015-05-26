#-*- coding:utf8 -*-
import pytz
import datetime
from django.utils import timezone
from celery import shared_task
from .models import ApplicantVacancyEvent
from notifications.models import Notification
from vacancies.models import  ApplicantVacancyApplicantVacancyStatus
from utils.functions import fromUTCtoLocal,fromLocaltoUTC


@shared_task
def check_events():
    current_time = datetime.datetime.now()
    events = ApplicantVacancyEvent.objects.all()
    #выбираем только те события, которые назначены на сегодня
    today_events = [e for e in events if fromUTCtoLocal(e.start).date() == current_time.date()]
    #добавляем к текущему времени временную зону, чтобы его можно было сравнить с datetime object из базы
    current_time = timezone.make_aware(current_time,timezone.get_default_timezone())
    for event in today_events:
        #если событие назначено на время в интервале 30 минут(от текущего момента), то создаём оповещение
        if abs(fromUTCtoLocal(event.start) - current_time) <= datetime.timedelta(minutes=60):
             message = "На " + str(fromUTCtoLocal(event.start).time()) + " назначено " + str(event.event)

             Notification.objects.create(message=message)
        #выбираем последний присвоенный статус по данной вакансии
        last_vacancy_status = ApplicantVacancyApplicantVacancyStatus.objects.filter(applicant_vacancy = event.applicant_vacancy).order_by('-pk')[0]
        #если событие произошло, а статус после этого не был изменён то, создаём оповещение
        if fromUTCtoLocal(last_vacancy_status.date) < fromUTCtoLocal(event.end) < current_time :
            message = 'Измените статус кандидата' + str(event.applicant_vacancy.applicant) + ' по вакансии ' + str(event.applicant_vacancy.vacancy.position)
            Notification.objects.create(message=message)
