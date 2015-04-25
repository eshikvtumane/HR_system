#-*- coding:utf8 -*-

import datetime
from django.utils import timezone
from celery import shared_task
from .models import ApplicantVacancyEvent
from notifications.models import Notification
from utils.functions import fromUTCtoLocal,fromLocaltoUTC

@shared_task
def check_events():
    current_time = timezone.now()
    events = ApplicantVacancyEvent.objects.all()
    #выбираем только те события, которые назначены на сегодня
    today_events = [e for e in events if fromUTCtoLocal(e.start).date() == current_time.date()]
    for event in today_events:
        print (fromUTCtoLocal(event.start))
        print(current_time)

        # if fromUTCtoLocal(event.start) <= current_time + datetime.timedelta(minutes=30):
        #     Notification.objects.create(message='У вас скоро состоится событие')
