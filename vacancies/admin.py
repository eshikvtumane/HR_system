#-*- coding: utf8 -*-

import datetime
from django.contrib import admin
from .models import Head, Department, VacancyStatus, Vacancy,VacancyStatusHistory, \
    ApplicantVacancy, \
    ApplicantVacancyStatus,\
    CurrentApplicantVacancyStatus


# Register your models here.
class HeadInline(admin.StackedInline):
    model = Head

class DepartmentAdmin(admin.ModelAdmin):
    inlines =(
        HeadInline,
    )
    fields = []

class VacancyStatusAdmin(admin.ModelAdmin):
    fields = []

class VacancyStatusHistoryAdmin(admin.ModelAdmin):
    fields = []


class VacancyStatusHistoryInline(admin.StackedInline):
    model = VacancyStatusHistory
    extra = 0

class VacancyAdmin(admin.ModelAdmin):
    inlines = (
        VacancyStatusHistoryInline,
    )
    fields = []
    readonly_fields = ('author',)

    def save_model(self,request,obj, form,change):
        obj.author = request.user
        obj.date_created = datetime.datetime.now()
        obj.save()
        vacancy_status = VacancyStatus.objects.get(name='Открыта')
        VacancyStatusHistory.objects.create(vacancy=obj,status=vacancy_status)
        return obj

class ApplicantVacancyAdmin(admin.ModelAdmin):
    fields = []

class  ApplicantVacancyStatusAdmin(admin.ModelAdmin):
    fields = []
    readonly_fields = ('author',)

    def save_model(self,request,obj, form,change):
        obj.author = request.user
        obj.date_created = datetime.datetime.now()
        obj.save()
        return obj

class ApplicantVacancyApplicantVacancyStatusAdmin(admin.ModelAdmin):
    fields = []

admin.site.register(Department, DepartmentAdmin)
admin.site.register(VacancyStatus, VacancyStatusAdmin)
admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(ApplicantVacancy,ApplicantVacancyAdmin)
admin.site.register(ApplicantVacancyStatus,ApplicantVacancyStatusAdmin)
admin.site.register(CurrentApplicantVacancyStatus, ApplicantVacancyApplicantVacancyStatusAdmin)
admin.site.register(VacancyStatusHistory, VacancyStatusHistoryAdmin)

