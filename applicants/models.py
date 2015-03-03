#-*- coding:utf8 -*-
from django.db import models

# Create your models here.
class Applicant(models.Model):
    class Meta:
        db_table = 'Applicants'
        verbose_name = 'Кандидат'
        verbose_name_plural = 'Кандидаты'

# ФИО
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)

# Фотография кандидата
    photo = models.FileField(upload_to='photo_applicants')

    

# контакты
    email = models.CharField(max_length=255)
    skype = models.CharField(max_length=30)
    icq =  models.CharField(max_length=10)

class Education(models.Model):
    class Meta:
        db_table = 'Educations'
        verbose_name = 'Образование'
        verbose_name_plural = 'Образование'

    type = models.CharField(max_length=255)
