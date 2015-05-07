from django.shortcuts import render_to_response
from django.views.generic import View
from django.template import RequestContext

# Create your views here.
class EmployeesView(View):
    template = 'employees/employees_view.html'
    def get(self, request):
        args = {}
        rc = RequestContext(request, args)
        return  render_to_response(self.template, rc)