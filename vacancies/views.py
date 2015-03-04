from django.shortcuts import render,render_to_response
from django.views.generic import View
from django.template import RequestContext
from forms import VacancyForm


class AddVacancy(View):
    template = 'vacancy_add.html'
    def get(self,request):
        form = VacancyForm()
        c = RequestContext(request,{'form':form})
        return render_to_response(self.template,c)


