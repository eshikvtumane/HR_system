from django.contrib import admin
from models import Education

# Register your models here.

class EducationAdmin(admin.ModelAdmin):
    fields = []

admin.site.register(Education, EducationAdmin)