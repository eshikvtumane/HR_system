#-*- coding: utf8 -*-
from applicants.models import  Position
from django.db import models

class Status(models.Model):
    class Meta:
        pass

    name = models.TextField(max_length=50)



class Vacancy(models.Model):
    class Meta:
        pass

    position = models.ForeignKey(Position)
    salary = models.FloatField()
    post_date = models.DateTimeField('Дата размещения')
    end_date = models.DateTimeField('Крайний срок')
    description = models.TextField()
    status = models.ForeignKey(Status)




