from django.contrib import admin
from models import Head, Department, Status

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

admin.site.register(Department, DepartmentAdmin)
admin.site.register(Status, StatusAdmin)
