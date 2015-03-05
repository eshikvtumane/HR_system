#-*- coding:utf8 -*-
from django.shortcuts import render, render_to_response
from django.views.generic import View
from django.template import RequestContext

from forms import ApplicantForm, ApplicantEducationForm
from models import Education, Major

# Create your views here.

# Добавление кандидата
class ApplicantAddView(View):
    template = 'applicant_add.html'
    def get(self, request):
        form = ApplicantForm()
        edu_form = ApplicantEducationForm

        edu = Education.objects.all()
        major = Major.objects.all()

        args = {}
        #args['applicant_form'] = form
        args['edu'] = edu
        args['majors'] = major
        rc = RequestContext(request, args)
        return render_to_response(self.template, rc)
