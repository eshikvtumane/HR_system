from django.shortcuts import render,render_to_response
from django.views.generic import View
from django.template import RequestContext
from forms import VacancyForm, DepartmentForm


class AddVacancy(View):
    template = 'vacancy_add.html'
    def get(self,request):
        vacancy_form = VacancyForm()
        department_form = DepartmentForm()
        c = RequestContext(request,{'vacancy_form':vacancy_form,
                                    'department_form':department_form})
        return render_to_response(self.template,c)


