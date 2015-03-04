#-*- coding: utf8 -*-

from django.db import models

class Position(models.Model):
    class Meta:
        pass




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
    description = models.TextField()
    status = models.ForeignKey(Status)



