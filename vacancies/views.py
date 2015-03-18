#-*- coding: utf8 -*-
from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from django.views.generic import View
from django.template import RequestContext
from forms import VacancyForm
from vacancies.models import Department, Head, Vacancy, Position, Status
import json
from django.core import serializers
import datetime


class AddVacancy(View):
    template = 'vacancies/vacancy_add.html'
    def get(self,request):
        vacancy_form = VacancyForm()
        departments  = Department.objects.all()
        c = RequestContext(request,{'vacancy_form':vacancy_form,
                                    'departments':departments}
                                    )
        return render_to_response(self.template,c)


    def post(self,request):
        if request.is_ajax:
            position = Position.objects.get(pk=int(request.POST['position']))
            salary = int(request.POST['salary'])
            end_date = datetime.datetime.strptime(request.POST['end_date'],
                                                  '%d-%m-%Y').date()
            description = str(request.POST['description'])
            head = Head.objects.get( pk = int(request.POST['head']))

            vacancy = Vacancy.objects.create(position=position,salary=salary,
                              end_date=end_date,description=description,
                              head=head)
            response = []
            response.append({'vacancy_id':vacancy.id})
            vacancy_id = json.dumps(response)
            return HttpResponse(vacancy_id)

class VacancyView(View):
    template = 'vacancies/vacancy_view.html'
    def get(self,request,id):
        vacancy = Vacancy.objects.get(pk=id)
        vacancy_form = VacancyForm(instance=vacancy)
        c = RequestContext(request,{'vacancy_form':vacancy_form,
                                    'vacancy':vacancy},
                           )
        return render_to_response(self.template, c)

    def post(self,request,id):
        post_data = request.POST.copy()
        post_data['end_date'] = datetime.datetime.strptime(post_data['end_date'],
                                                   '%d-%m-%Y').date()

        print post_data['end_date']
        vacancy = Vacancy.objects.get(pk=id)
        vacancy_form = VacancyForm(post_data,instance=vacancy)

        try:
            vacancy_form.is_valid()
            print vacancy_form.errors
            vacancy_form.save()
        except:
            raise TypeError("Данные не корректны!")
        return HttpResponse("200")


###AJAX REQUESTS#################
def get_heads_ajax(request):
    if request.is_ajax:
        department_id = int(request.GET['department'])
        heads = list(Head.objects.filter(department=department_id).values('id','name'))
        heads = json.dumps(heads)
        return HttpResponse(heads,content_type='application/json')


###############################


