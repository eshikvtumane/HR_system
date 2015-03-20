#-*- coding: utf8 -*-
from applicants.models import Position, Applicant
from django.db import models
import datetime
from time import timezone

####HELPER FUNCTIONS##########


##############################



####HELPER CLASSES###########

# class ConvertedDateTime(models.DateTimeField):
#     def get_prep_value(self, value):
#         return str(datetime.datetime.strptime(value,'%d-%m-%Y'))

##############################################

#####CONSTANTS############
DEFAULT_VACANCY_STATUS = 1
DEFAULT_APPLICANT_VACANCY_STATUS = 1


#######################

class Status(models.Model):
    class Meta:
        db_table = 'Statuses'
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

    name = models.TextField(max_length=50)

    def __unicode__(self):
        return self.name




class Department(models.Model):
    class Meta:
        db_table = 'Departments'
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'

    name = models.CharField(verbose_name=u"Название отдела",max_length=50)

    def __unicode__(self):
        return self.name

#Руководители отделов компании
class Head(models.Model):
    class Meta:
        db_table = 'Heads'
        verbose_name = 'Руководитель'
        verbose_name_plural = 'Руководители'

    name = models.TextField()
    department = models.ForeignKey(Department)

    def __unicode__(self):
        return self.name





class Vacancy(models.Model):
    class Meta:
        db_table = 'Vacancies'
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'


    salary = models.FloatField(verbose_name=u"Заработная плана")
    published_at = models.DateTimeField(verbose_name=u'Дата размещения',
                                    default=datetime.datetime.now())
    end_date = models.DateTimeField(verbose_name=u'Крайний срок')
    description = models.TextField(verbose_name=u"Описание")
    head =  models.ForeignKey(Head,verbose_name=u"Руководитель")

    status = models.ForeignKey(Status,verbose_name=u'Статус',
                               default=DEFAULT_VACANCY_STATUS)
    position = models.ForeignKey(Position,verbose_name=u'Должность' )

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in
                Vacancy._meta.fields]


class ApplicantVacancyStatus(models.Model):
    class Meta:
        db_table = 'ApplicantVacancyStatuses'
        verbose_name = 'Статус кандидата по вакансии'
        verbose_name_plural = 'Статусы кандидата по вакансии'
    name = models.TextField()

    def __unicode__(self):
        return self.name



class Event(models.Model):
    class Meta:
        db_table = 'Events'
        verbose_name = 'Событие'
        verbose_name_plural = 'События'


    name = models.CharField(max_length=50,verbose_name="Название события")
    date_time = models.DateTimeField(verbose_name='Дата назначения')
    subject = models.ForeignKey('ApplicantVacancy')



# Отношение Кандидат-Вакансии
class ApplicantVacancy(models.Model):
    class Meta:
        db_table = 'ApplicantVacancies'
        verbose_name = 'Вакансия кандидата'
        verbose_name_plural = 'Вакансии кандидата'

    applicant = models.ForeignKey(Applicant)
    vacancy = models.ForeignKey('Vacancy')
    salary = models.FloatField(verbose_name='Запрашиваемая сумма')
    suggested_salary = models.FloatField(verbose_name='Предлагаемая сумма')
    create_date = models.DateField(default=datetime.datetime.now(), verbose_name='Дата добавления')
    status = models.ForeignKey(ApplicantVacancyStatus, default =
    DEFAULT_APPLICANT_VACANCY_STATUS)


