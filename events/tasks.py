#-*- coding:utf8 -*-

import datetime
from celery import shared_task
from .models import ApplicantVacancyEvent
from utils.functions import fromUTCtoLocal,fromLocaltoUTC

@shared_task
def check_events():
    current_time = datetime.datetime.now()
    events = ApplicantVacancyEvent.objects.all()
    #выбираем только те события, которые назначены на сегодня
    today_events = [e for e in events if fromUTCtoLocal(e.start).date() == current_time.date()]
    for event in today_events:
        if fromUTCtoLocal(event.start) <= current_time + datetime.timedelta(minutes=30):
            print "У вас скоро состоится событие"
        else:
            "fdfdffdfd"