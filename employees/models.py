# -*- coding:utf-8 -*-
from django.db import models
from applicants.models import Applicant, Position
from vacancies.models import Head
from django.utils import timezone

# Create your models here.
class Employee(models.Model):
    class Meta:
        db_table = 'Employees'
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    applicant = models.ForeignKey(Applicant)
    position = models.ForeignKey(Position)
    head = models.ForeignKey(Head)
    admission_date = models.DateTimeField(default=timezone.now())
    dismissal = models.DateTimeField(blank=True, null=True)