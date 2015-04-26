#-*- coding:utf8 -*-

import datetime
from django.utils import timezone
from celery import shared_task
from .models import ApplicantVacancyEvent
from notifications.models import Notification
from utils.functions import fromUTCtoLocal,fromLocaltoUTC
import pytz

@shared_task
def check_events():
    current_time = datetime.datetime.now()
    events = ApplicantVacancyEvent.objects.all()
    #выбираем только те события, которые назначены на сегодня
    today_events = [e for e in events if fromUTCtoLocal(e.start).date() == current_time.date()]
    current_time = timezone.make_aware(current_time,timezone.get_default_timezone())
    for event in today_events:
        if fromUTCtoLocal(event.start) - current_time <= datetime.timedelta(minutes=30):
             message = "На " + str(fromUTCtoLocal(event.start).time()) + " назначено " + str(event.event)
             Notification.objects.create(message=message)


