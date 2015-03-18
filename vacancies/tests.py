#-*- coding: utf8 -*-
from django.test import TestCase
from vacancies.models import Status, Head, Department, Vacancy
from applicants.models import Position
import datetime

# Create your tests here



#######MODEL TESTING#######
class VacancyTest(TestCase):
    def test_adding_vacancy_to_db(self):
        department = Department.objects.create(name="Отдел маркетинга")
        head = Head.objects.create(name='Василиса Петровна',department=department)
        status = Status.objects.create(name="Открыта")
        position = Position.objects.create(name="Продажник")
        vacancy = Vacancy.objects.create(salary=5000,end_date=datetime.datetime(
            2015,5,4),description="Классная вакансия",head = head,position =
        position)

    def test_saving_vacancy_via_ajaxpost_request(self):
        self.client.post('vacancies/add')





