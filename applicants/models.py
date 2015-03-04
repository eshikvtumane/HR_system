#-*- coding:utf8 -*-
from django.db import models
from datetime import datetime

# Create your models here.



# Кандидат
class Applicant(models.Model):
    class Meta:
        db_table = 'Applicants'
        verbose_name = 'Кандидат'
        verbose_name_plural = 'Кандидаты'

    # ФИО
    first_name = models.CharField(max_length=255, verbose_name='Фамилия')
    last_name = models.CharField(max_length=255, verbose_name='Имя')
    middle_name = models.CharField(max_length=255, verbose_name='Отчество', null=True, blank=True)

    # Дата рождения
    birthday = models.DateField(verbose_name='Дата рождения')

    # Фотография кандидата
    photo = models.FileField(upload_to='photo_applicants', verbose_name='Фото кандидата', null=True, blank=True)



    # Место жительства
    region = models.TextField()
    city = models.TextField()
    street = models.TextField()
    building = models.TextField()
    # корпус
    housing = models.TextField(null=True, blank=True)
    # строение
    structure = models.TextField(null=True, blank=True)
    flat = models.IntegerField(max_length=5)

    # Должность
    position = models.ManyToManyField('Position', verbose_name='Должность')

    experience = models.FloatField(verbose_name='Стаж', null=True, blank=True)

    # контакты
    phone = models.IntegerField(max_length=10, verbose_name='Мобильный телефон')
    email = models.CharField(max_length=255, verbose_name='Email', null=True, blank=True)
    skype = models.CharField(max_length=32, verbose_name='Skype', null=True, blank=True)
    icq = models.IntegerField(max_length=10, verbose_name='ICQ', null=True, blank=True)


# Образование
class Education(models.Model):
    class Meta:
        db_table = 'Educations'
        verbose_name = 'Образование'
        verbose_name_plural = 'Образование'

    # Тип образования (высшее, неполное, заочное)
    type = models.CharField(max_length=255, verbose_name='Тип')

    def __unicode__(self):
        return self.type


# Специальность
class Major(models.Model):
    class Meta:
        db_table = 'Majors'
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'

    # Название специальности
    name = models.TextField(verbose_name='Специальность')


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



# Предпочитаемые должности для кандидата
class ApplicantToPosition(models.Model):
    class Meta:
        db_table = 'ApplicantToPositions'
        verbose_name = 'Предполагаемая должность'
        verbose_name_plural = 'Предполагаемые долности'

    # Кандидат
    applicant = models.ForeignKey('Applicant')
    # Название должности
    position = models.ForeignKey('Position')

    # Запрашиваемая зарплата
    salary = models.FloatField()

    # Дата создания
    date_create = models.DateTimeField(default=datetime.now())



# Должность
class Position(models.Model):
    class Meta:
        db_table = 'Positions'
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'

    name = models.TextField(verbose_name='Должность')

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


