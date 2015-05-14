#-*- coding:utf8 -*-
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

# Кандидат
class Applicant(models.Model):
    class Meta:
        db_table = 'Applicants'
        verbose_name = 'Кандидат'
        verbose_name_plural = 'Кандидаты'

    GENDER_LIST = (
        ('1', 'Мужской'),
        ('2', 'Женский'),
    )
    # ФИО
    first_name = models.CharField(max_length=255, verbose_name='Фамилия')
    last_name = models.CharField(max_length=255, verbose_name='Имя')
    middle_name = models.CharField(max_length=255, verbose_name='Отчество', null=True, blank=True)
    sex = models.CharField(max_length=1, choices=GENDER_LIST, verbose_name='Пол', null=True, blank=True)

    # Дата рождения
    birthday = models.DateField(verbose_name='Дата рождения',null=True,blank=True)

    # Фотография кандидата
    photo = models.FileField(upload_to='photo_applicants', default='default.gif', verbose_name='Фото кандидата', null=True, blank=True)

    # Место жительства
    city = models.TextField(verbose_name='Город', null=True, blank=True)
    street = models.TextField(verbose_name='Улица', null=True, blank=True)
    building = models.TextField(verbose_name='Номер дома', null=True, blank=True)

    # Стаж
    #experience = models.FloatField(verbose_name='Стаж', null=True, blank=True)

    # контакты
    #phone = models.IntegerField(max_length=10, verbose_name='Мобильный телефон')
    email = models.CharField(max_length=255, verbose_name='Email', null=True, blank=True)
    skype = models.CharField(max_length=32, verbose_name='Skype', null=True, blank=True)
    icq = models.IntegerField(max_length=10, verbose_name='ICQ', null=True, blank=True)

    # Соц. сети
    vk = models.URLField(verbose_name='ВКонтакте',null=True, blank=True)
    fb = models.URLField(verbose_name='Facebook', null=True, blank=True)

    # Источник
    #source = models.ForeignKey('SourceInformation', verbose_name='Источник')

    note = models.TextField(verbose_name='Примечание', null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')

    def __unicode__(self):
        return '%s %s %s' % (self.first_name, self.last_name, self.middle_name)

    def getFullName(self):
        return '%s %s %s' % (self.first_name, self.last_name, self.middle_name)



class Phone(models.Model):
    class Meta:
        db_table = 'Phones'
        verbose_name = 'Телефон'
        verbose_name_plural = 'Телефоны'

    applicant = models.ForeignKey('Applicant')
    phone = models.IntegerField(verbose_name='Номер телефона', max_length=11)

    def __unicode__(self):
        return str(self.phone)


# Образование
class Education(models.Model):
    class Meta:
        db_table = 'Educations'
        verbose_name = 'Образование'
        verbose_name_plural = 'Образование'

    # Тип образования (высшее, неполное, заочное)
    type = models.CharField(max_length=255, verbose_name='Тип')
    author = models.ForeignKey(User, verbose_name='Автор')
    date_created = models.DateTimeField(default=datetime.now(), verbose_name='Дата добавления')

    def __unicode__(self):
        return self.type

    #def save(self, *args, **kwargs):
#


# Специальность
class Major(models.Model):
    class Meta:
        db_table = 'Majors'
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'

    # Название специальности
    name = models.TextField(verbose_name='Специальность')
    author = models.ForeignKey(User)
    date_created = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return self.name



# Отношение Кандидат-Образование
class ApplicantEducation(models.Model):
    class Meta:
        db_table = 'ApplicantEducations'
        verbose_name = 'Образование кандидата'
        verbose_name_plural = 'Образование кандидатов'

    # Кандидат
    applicant = models.ForeignKey('Applicant')
    # Образование кандидата (может быть много)
    education = models.ForeignKey('Education', verbose_name='Образование')
    # Специальность
    major = models.ForeignKey('Major', verbose_name='Специальность')
    # Год начала учёбы
    study_start = models.IntegerField(max_length=4, verbose_name='Начало учёбы')
    # Год окончания учёбы
    study_end = models.IntegerField(max_length=4, verbose_name='Окончание учёбы')



# Должность
class Position(models.Model):
    class Meta:
        db_table = 'Positions'
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'

    name = models.TextField(verbose_name='Должность')
    author = models.ForeignKey(User)
    date_created = models.DateTimeField(default=datetime.now())


    def __unicode__(self):
        return self.name


# Хранение резюме
class Resume(models.Model):
    class Meta:
        db_table = 'Resume'
        verbose_name = 'Резюме'
        verbose_name_plural = 'Резюме'

    # Кандидат
    applicant = models.ForeignKey('Applicant')
    # файл резюме
    resume_file = models.FileField(upload_to='resume', verbose_name='Резюме')
    # Дата добавления
    date_upload = models.DateTimeField(default=datetime.now(), verbose_name='Дата загрузки')

class Portfolio(models.Model):
    '''
         Работы кандидата
    '''
    class Meta:
        db_table = 'Portfolio'
        verbose_name = 'Портфолио'
        verbose_name_plural = 'Портфолио'

    applicant = models.ForeignKey('Applicant')
    portfolio_file = models.FileField(upload_to='portfolio')
    date_upload = models.DateTimeField(default=datetime.now(), verbose_name='Дата загрузки')

class SourceInformation(models.Model):
    '''
         Источник информации (место, откуду кандидат узнал о наличии данной вакансии)
    '''
    class Meta:
        db_table = 'SourceInformations'
        verbose_name = 'Источник'
        verbose_name_plural = 'Источники'

    source = models.CharField(max_length=100)
    author = models.ForeignKey(User)
    date_created = models.DateTimeField(default=datetime.now(), verbose_name='Дата создания')

    def __unicode__(self):
        return self.source


# Хранение истории изменений информации о кандидате
class HistoryChangeApplicantInfo(models.Model):
    class Meta:
        db_table='HistoryChangeApplicants'
        verbose_name = 'История изменений'
        verbose_name_plural = 'Истории изменений'

    # кто изменил анкету
    user = models.ForeignKey(User)
    # чью анкету изменили
    applicant = models.ForeignKey('Applicant')
    # тип изменения
    type_change = models.TextField(default='')
    # когда изменил
    date_change = models.DateTimeField(default=datetime.now())
