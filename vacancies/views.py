#-*- coding: utf8 -*-
from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from django.views.generic import View
from django.template import RequestContext
from forms import VacancyForm
from vacancies.models import Department, Head
import json
import simplejson
from django.core import serializers


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
            print request.POST['position']
            print request.POST['description']





###AJAX REQUESTS#################
def get_heads_ajax(request):
    if request.is_ajax:
        department_id = int(request.GET['department'])
        heads = list(Head.objects.filter(department=department_id).values('id','name'))
        heads = simplejson.dumps(heads)
        return HttpResponse(heads,content_type='application/json')

###############################

