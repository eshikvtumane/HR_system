from django.contrib import admin
from models import Education, Major, SourceInformation, Applicant, Resume, Portfolio, Position
from vacancies.models import Vacancy

# Register your models here.

class ResumeInline(admin.StackedInline):
    model = Resume

class PortfolioInline(admin.StackedInline):
    model = Portfolio

class EducationAdmin(admin.ModelAdmin):
    fields = []

class MajorAdmin(admin.ModelAdmin):
    fields = []

class SourceAdmin(admin.ModelAdmin):
    fields = []

class ApplicantAdmin(admin.ModelAdmin):
    inlines = (
        ResumeInline,
        PortfolioInline
    )
    fields = []

class VacancyInline(admin.StackedInline):
    model = Vacancy

class PositionAdmin(admin.ModelAdmin):
    inlines = (
        VacancyInline,
    )
    fields = []

admin.site.register(Education, EducationAdmin)
admin.site.register(Major, MajorAdmin)
admin.site.register(SourceInformation, SourceAdmin)
admin.site.register(Applicant, ApplicantAdmin)
admin.site.register(Position, PositionAdmin)