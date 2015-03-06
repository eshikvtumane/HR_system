from django.forms import ModelForm
from models import Vacancy,Department

class VacancyForm(ModelForm):
    class Meta:
        model = Vacancy
        fields = ("position","salary",'post_date',"end_date","description",
                  )

class DepartmentForm(ModelForm):
    class Meta:
        model = Department
