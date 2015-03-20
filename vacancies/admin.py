from django.contrib import admin
from models import Head, Department, Status, ApplicantVacancyStatus

# Register your models here.
class HeadInline(admin.StackedInline):
    model = Head

class DepartmentAdmin(admin.ModelAdmin):
    inlines =(
        HeadInline,
    )
    fields = []

class StatusAdmin(admin.ModelAdmin):
    fields = []

class ApplicantVacancyStatusAdmin(admin.ModelAdmin):
    fields = []

admin.site.register(Department, DepartmentAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(ApplicantVacancyStatus, ApplicantVacancyStatusAdmin)
