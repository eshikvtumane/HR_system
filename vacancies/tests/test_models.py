#-*- coding: utf8 -*-
from django.test import TestCase
from vacancies.models import Status, Head, Department, Vacancy
from applicants.models import Position
import datetime
from unittest import skip

# Create your tests here
def create_vacancy():
    department = Department.objects.create(name="Отдел маркетинга")
    head = Head.objects.create(name='Василиса Петровна',department=department)
    status = Status.objects.create(name="Открыта")
    position = Position.objects.create(name="Продажник")
    vacancy = Vacancy(salary=5000,end_date=datetime.datetime(2015,5,4),
                                     description="Классная вакансия",head = head,position = position)
    return vacancy
@skip
class VacancyTest(TestCase):
    def test_adding_vacancy_to_db(self):
        vacancy = create_vacancy()
        vacancy.save()


    def test_saving_vacancy_via_ajaxpost_request(self):
        self.client.post('vacancies/add')






