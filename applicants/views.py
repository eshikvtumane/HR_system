#-*- coding:utf8 -*-
from django.shortcuts import render, render_to_response
from django.views.generic import View

from forms import ApplicantForm, ApplicantEducationForm

# Create your views here.

# Добавление кандидата
class ApplicantAddView(View):
    template = 'applicant_add.html'
    def get(self, request):
        form = ApplicantForm()
        edu_form = ApplicantEducationForm
        args = {}
        args['applicant_form'] = form
        args['edu_form'] = edu_form
        return render_to_response(self.template, args)
