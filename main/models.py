#-*- coding:utf-8 -*-
from django.db import models
from datetime import datetime

from django.contrib.auth.models import User

# Create your models here.
class Todo(models.Model):
    class Meta:
        db_table = 'Notes'
        verbose_name = 'Запись'
        verbose_name_plural = 'Записки'

    user = models.ForeignKey(User)
    todo = models.TextField()
    date_create = models.DateTimeField(default=datetime.now())
