#-*- coding: utf8 -*-
from applicants.models import Position, Applicant
from django.db import models
import datetime
from time import timezone

####HELPER FUNCTIONS##########
def defaultStatus():
    return Status.objects.get(name='Открыта')

##############################

####HELPER CLASSES###########

# class ConvertedDateTime(models.DateTimeField):
#     def get_prep_value(self, value):
#         return str(datetime.datetime.strptime(value,'%d-%m-%Y'))

##############################################



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



DEFAULT_VACANCY_STATUS = 1

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

