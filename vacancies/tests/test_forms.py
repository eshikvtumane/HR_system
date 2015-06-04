#-*- coding: utf8 -*-

from django.test import TestCase
from vacancies.models import Status, Head, Department, Vacancy
from applicants.models import Position
import datetime
from test_models import create_vacancy

from vacancies.forms import AddVacancyForm, EditVacancyForm
from vacancies.models import  Head
class VacancyFormTest(TestCase):
    def test_vacancy_form_validation_at_addition(self):
        dep = Department.objects.create(name='Отдел продаж')
        Position.objects.create(name='Программист')
        Status.objects.create(name='Открыта')
        Head.objects.create(name='Df',department=dep)
        form = AddVacancyForm({'salary':200.0,'end_date':datetime.datetime(2015,3,4),'description':"fdgdg",
                            'position':1,'head':1})
        form.is_valid()

        form.save()

        self.assertEqual(Vacancy.objects.count(),1)

    def test_vacancy_form_validation_at_update(self):
        vacancy = create_vacancy()
        vacancy.save()

        form = EditVacancyForm({'salary':200.0,'end_date':datetime.datetime(2015,3,4),'description':"fdgdg",
                            'position':1,'status': 1},instance=vacancy)
        form.is_valid()

        form.save()




