#-*- coding: utf8 -*-
from applicants.models import Position
from django.db import models

class Status(models.Model):
    class Meta:
        pass

    name = models.TextField(max_length=50)



class Department(models.Model):
    class Meta:
        pass

    name = models.CharField(verbose_name=u"Название отдела",max_length=50)




#Руководители отделов компании
class Head(models.Model):
    class Meta:
        pass

    name = models.TextField()
    department = models.ForeignKey(Department)


class Vacancy(models.Model):
    class Meta:
        pass

    salary = models.FloatField(verbose_name=u"Заработная плана")
    post_date = models.DateTimeField(verbose_name=u'Дата размещения')
    end_date = models.DateTimeField(verbose_name=u'Крайний срок')
    description = models.TextField(verbose_name=u"Описание")
    head =  models.ForeignKey(Head,verbose_name=u"Руководитель")
    status = models.ForeignKey(Status,verbose_name=u'Статус')
    position = models.ForeignKey(Position,verbose_name=u'Должность' )




