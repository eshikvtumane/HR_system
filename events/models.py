#-*- coding:utf8 -*-
from django.db import models
from django.contrib.auth.models import User
from vacancies.models import ApplicantVacancy




#Событие, связанное с кандидатом
class Event(models.Model):
    class Meta:
        db_table = 'Events'
        verbose_name = 'Событие'
        verbose_name_plural = 'События'


    name = models.CharField(max_length=50,verbose_name="Название события")
    def __unicode__(self):
        return self.name



class ApplicantVacancyEvent(models.Model):
    class Meta:
        db_table = "ApplicantVacancyEvents"
        verbose_name = "Запланированное событие"
        verbose_name_plural = 'Запланированные события'


    start = models.DateTimeField(verbose_name="Начало события")
    end = models.DateTimeField(verbose_name="Окончание события")
    applicant_vacancy = models.ForeignKey(ApplicantVacancy)
    event = models.ForeignKey('Event')
    happened = models.BooleanField(default=False)
    author = models.ForeignKey(User,verbose_name='Автор')


