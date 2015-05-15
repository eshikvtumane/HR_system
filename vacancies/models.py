#-*- coding: utf8 -*-
from applicants.models import Position, Applicant, SourceInformation, Education

from django.contrib.auth.models import User
from django.db import models
import datetime
from django.utils import timezone

#####CONSTANTS############
DEFAULT_VACANCY_STATUS = 1
DEFAULT_APPLICANT_VACANCY_STATUS = 1


#######################
#Словарь статусов вакансий
class VacancyStatus(models.Model):
    class Meta:
        db_table = 'VacancyStatuses'
        verbose_name = 'Статус вакансии'
        verbose_name_plural = 'Статусы вакансии'

    name = models.TextField(max_length=50)
    icon_class = models.CharField(max_length=30, default='')

    def __unicode__(self):
        return self.name

#Словарь отделов компаний
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


    GENDER_LIST = (
        ('1', 'Мужской'),
        ('2', 'Женский'),
    )

    MARRIAGE_STATUS_LIST = (
        ('1', 'В браке'),
        ('2', 'Холост'),
    )
    salary = models.FloatField(verbose_name=u"Заработная плата")
    sex =  models.CharField(max_length=1, choices=GENDER_LIST, verbose_name='Пол', null=True, blank=True)
    published_at = models.DateTimeField(verbose_name=u'Дата размещения',
                                    default=timezone.now)
    marriage_status = models.CharField(max_length=1, verbose_name=u'Семейный статус',choices=MARRIAGE_STATUS_LIST, null=True,blank=True)
    duties = models.TextField(verbose_name=u'Обязанности',null=True,blank=True)
    end_date = models.DateField(verbose_name=u'Предполагаемый срок закрытия',null=True,blank=True)
    additional_info = models.TextField(verbose_name=u"Дополнительная информация",null=True,blank=True)
    skills = models.TextField(verbose_name=u"Необходимые навыки",null=True,blank=True)
    creation_reason = models.TextField(verbose_name=u'Причина появления вакансии',null=True,blank=True)
    head =  models.ForeignKey(Head,verbose_name=u"Руководитель")
    position = models.ForeignKey(Position,verbose_name=u'Должность' )
    author = models.ForeignKey(User,verbose_name=u'Автор')
    advancement = models.TextField(verbose_name=u'Карьерный рост',null=True,blank=True)
    education = models.ForeignKey(Education,verbose_name='Требуемое образование',null=True,blank=True)
    further_education = models.TextField(verbose_name=u'Возможность обучения/стажировок',null=True,blank=True)
    paid_vacation = models.IntegerField(verbose_name=u'Оплачиваемый отпуск(кол-во дней)',null=True,blank=True)
    last_status = models.ForeignKey('VacancyStatus', default=DEFAULT_VACANCY_STATUS)

    
    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in
                Vacancy._meta.fields]


    def __unicode__(self):
        return self.position.name + " " + str(self.published_at)

# Ведение истории по изменению статуса у вакансии
class VacancyStatusHistory(models.Model):
    class Meta:
        db_table = 'VacancyStatusHistory'
        verbose_name = 'История изменения статуса вакансии'
        verbose_name_plural = 'История изменения статуса вакансии'

    vacancy = models.ForeignKey('Vacancy')
    status = models.ForeignKey('VacancyStatus', default=DEFAULT_VACANCY_STATUS)
    date_change = models.DateTimeField(verbose_name=u'Дата изменения',
                                    default=timezone.now)


#Словарь статусов для отношения Кандидат-Вакансия
class ApplicantVacancyStatus(models.Model):
    class Meta:
        db_table = 'ApplicantVacancyStatuses'
        verbose_name = 'Статус кандидата по вакансии'
        verbose_name_plural = 'Статусы кандидата по вакансии'
    name = models.TextField(verbose_name='Статус')
    author = models.ForeignKey(User, verbose_name='Автор')
    date_created = models.DateTimeField('Дата создания', default=datetime.datetime.now())

    def __unicode__(self):
        return self.name


# Отношение Кандидат-Вакансии
class ApplicantVacancy(models.Model):
    class Meta:
        db_table = 'ApplicantVacancies'
        verbose_name = 'Вакансия кандидата'
        verbose_name_plural = 'Вакансии кандидата'

    applicant = models.ForeignKey(Applicant)
    vacancy = models.ForeignKey('Vacancy')
    source = models.ForeignKey(SourceInformation)
    salary = models.FloatField(verbose_name='Запрашиваемая сумма')
    suggested_salary = models.FloatField(verbose_name='Предлагаемая сумма')
    create_date = models.DateField(default=timezone.now, verbose_name='Дата добавления')

    def __unicode__(self):
        return "%s %s %s %s %s"%(self.vacancy.position.name,str(
            self.vacancy.published_at),self.applicant.first_name,
               self.applicant.last_name,self.applicant.middle_name)


#Текущий статус кандидата по вакансии
class ApplicantVacancyApplicantVacancyStatus(models.Model):
    class Meta:
        db_table = "ApplicantVacancyApplicantVacancyStatus"
        verbose_name = 'Текущий статус кандидата по вакансии'
        verbose_name_plural = 'Текущий статус кандидата по вакансии'

    applicant_vacancy = models.ForeignKey('ApplicantVacancy')
    applicant_vacancy_status = models.ForeignKey('ApplicantVacancyStatus',default =
    DEFAULT_APPLICANT_VACANCY_STATUS)
    date = models.DateTimeField(verbose_name='Дата присвоения',default=timezone.now)
    author = models.ForeignKey(User,verbose_name='Автор')
    note = models.TextField(verbose_name='Примечание',blank=True,null=True)





class Benefit(models.Model):
    class Meta:
        db_table = "Benefit"
        verbose_name = "Льгота"
        verbose_name_plural = "Льготы"

    name = models.CharField(max_length=100)


class VacancyBenefit(models.Model):
    class Meta:
        db_table = "VacancyBenefit"
        verbose_name = "Льгота по вакансии"
        verbose_name_plural = "Льготы по вакансии"


    vacancy = models.ForeignKey(Vacancy)
    benefit = models.ForeignKey(Benefit)


