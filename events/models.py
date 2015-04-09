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


    name = models.CharField(max_length=50,verbose_name="Название действия")
    def __unicode__(self):
        return self.name



class ApplicantVacancyEvent(models.Model):
    class Meta:
        db_table = "ApplicantVacancyEvents"
        verbose_name = "Назначенное действие"
        verbose_name_plural = 'Назначенное действие'


    start = models.DateTimeField(verbose_name="Начало")
    end = models.DateTimeField(verbose_name="Окончание")
    applicant_vacancy = models.ForeignKey(ApplicantVacancy)
    event = models.ForeignKey('Event')
    happened = models.BooleanField(default=False)
    author = models.ForeignKey(User,verbose_name='Автор')
    description = models.TextField(verbose_name='Описание',blank=True)

    def __unicode__(self):

        result_string = '{event} назначено по вакансии {vacancy} для {applicant} на {start} - {end}'.format(event=str(
            self.event),vacancy = str(self.applicant_vacancy.vacancy.position),applicant =
        str(self.applicant_vacancy.applicant),start=str(self.start), end=str( self.end))

        return result_string.decode('utf-8')


