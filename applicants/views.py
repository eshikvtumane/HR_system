from django.shortcuts import render, render_to_response
from django.views.generic import View

# Create your views here.
class ApplicantAddView(View):
    template = ''
    def get(self, request):
        return render_to_response()