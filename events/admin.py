from django.contrib import admin
from .models import Event, ApplicantVacancyEvent
# Register your models here.

class EventAdmin(admin.ModelAdmin):
    fields = []

class ApplicantVacancyEventAdmin(admin.ModelAdmin):
    fields = []

admin.site.register(Event,EventAdmin)
admin.site.register(ApplicantVacancyEvent,ApplicantVacancyEventAdmin)
