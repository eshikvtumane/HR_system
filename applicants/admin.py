from django.contrib import admin
from models import Education, Major

# Register your models here.

class EducationAdmin(admin.ModelAdmin):
    fields = []

class MajorAdmin(admin.ModelAdmin):
    fields = []

admin.site.register(Education, EducationAdmin)
admin.site.register(Major, MajorAdmin)