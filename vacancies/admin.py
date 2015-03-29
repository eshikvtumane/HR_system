from django.contrib import admin
from .models import Head, Department, VacancyStatus, Vacancy, ApplicantVacancy, \
    ApplicantVacancyStatus,Event,ApplicantVacancyEvent, \
    ApplicantVacancyApplicantVacancyStatus

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

class VacancyAdmin(admin.ModelAdmin):
    fields = []

class ApplicantVacancyAdmin(admin.ModelAdmin):
    fields = []

class  ApplicantVacancyStatusAdmin(admin.ModelAdmin):
    fields = []


class EventAdmin(admin.ModelAdmin):
    fields = []


class  ApplicantVacancyEventAdmin(admin.ModelAdmin):
    fields = []

class ApplicantVacancyApplicantVacancyStatusAdmin(admin.ModelAdmin):
    fields = []

admin.site.register(Department, DepartmentAdmin)
admin.site.register(VacancyStatus, VacancyStatusAdmin)
admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(ApplicantVacancy,ApplicantVacancyAdmin)
admin.site.register(ApplicantVacancyStatus,ApplicantVacancyStatusAdmin)
admin.site.register(Event,EventAdmin)
admin.site.register(ApplicantVacancyEvent,ApplicantVacancyEventAdmin)
admin.site.register(ApplicantVacancyApplicantVacancyStatus, ApplicantVacancyApplicantVacancyStatusAdmin)


