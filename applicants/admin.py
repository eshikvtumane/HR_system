#-*- coding:utf8 -*-
from django.contrib import admin
from models import Education, Major, SourceInformation, Applicant, Resume, Portfolio, Position, Phone, ApplicantEducation
from vacancies.models import Vacancy, ApplicantVacancy, ApplicantVacancyApplicantVacancyStatus
from datetime import datetime, date, timedelta

# Register your models here.
class YesterdayListFilter(admin.SimpleListFilter):
    title = 'Выборка по дате создания'
    parameter_name = 'yesterday'

    def lookups(self, request, model_admin):
        return (
            ('today', 'Сегодня'),
            ('yesterday', 'Вчера'),
            ('week', 'Последние 7 дней'),
            ('month', 'Этот месяц'),
            ('year', 'Этот год')
        )

    def queryset(self, request, queryset):
        today = date.today()
        if self.value() =='today':
            return self.__generalQS(queryset, today)

        if self.value() == 'yesterday':
            date_yest = today - timedelta(1)
            return self.__generalQS(queryset, date_yest)

        if self.value() == 'week':
            date_start = today - timedelta(7)
            return self.__rangeQS(queryset, date_start)

        if self.value() == 'month':
            date_start = date(today.year, today.month, 1)
            return self.__rangeQS(queryset, date_start)

        if self.value() == 'year':
            date_start = date(today.year, 1, 1)
            return self.__rangeQS(queryset, date_start)


    def __generalQS(self, qs, date_day):
        return qs.filter(
            date_created__day=date_day.day,
            date_created__month=date_day.month,
            date_created__year=date_day.year,
        )
    def __rangeQS(self, qs, date_day):
        return qs.filter(
            date_created__gte=date_day,
        )

class BaseAdmin(admin.ModelAdmin):
    change_list_template = "admin/change_list_filter_sidebar.html"
    readonly_fields = ('author', 'date_created',)
    list_filter = ('author', 'date_created')


    def get_author(self, obj):
        return '<a href="/admin/auth/user/%s"><b>%s %s - %s</b></a>' % (
            obj.author.id, obj.author.first_name,
            obj.author.last_name,
            obj.author.username
        )
    get_author.short_description = 'Автор'
    get_author.allow_tags = True

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.date_created = datetime.now()
        obj.save()

        return obj

class BaseInline(admin.StackedInline):
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)


class ResumeInline(BaseInline):
    model = Resume
    extra = 0

class PortfolioInline(BaseInline):
    model = Portfolio
    extra = 0

class EducationAdmin(BaseAdmin):
    fields = ['type', 'author', 'date_created']
    list_display = ('id', 'get_type', 'get_author', 'date_created',)
    search_fields = ('type',)

    def get_type(self, obj):
        return '<a href="/admin/applicants/education/%s"><b>%s</b></a>' % (obj.id, obj.type)

    get_type.short_description = 'Тип образования'
    get_type.allow_tags = True


class MajorAdmin(BaseAdmin):
    fields = ['name', 'author', 'date_created']
    list_display = ('id', 'get_name', 'get_author', 'date_created')
    search_fields = ('name',)

    def get_name(self, obj):
        return '<a href="/admin/applicants/major/%s"><b>%s</b></a>' % (obj.id, obj.name)


    get_name.short_description = 'Специальность'
    get_name.allow_tags = True


class SourceAdmin(BaseAdmin):
    fields = ['source', 'author', 'date_created']
    list_display = ('id', 'get_source', 'get_author', 'date_created')
    search_fields = ('source',)

    def get_source(self, obj):
        return '<a href="/admin/applicants/sourceinformation/%s"><b>%s</b></a>' % (obj.id, obj.source)


    get_source.short_description = 'Источник'
    get_source.allow_tags = True




class PhoneInline(BaseInline):
    model = Phone
    extra = 0

class ApplicantEducationInline(BaseInline):
    model = ApplicantEducation
    extra = 0

class ApplicantAdmin(admin.ModelAdmin):
    change_list_template = "admin/change_list_filter_sidebar.html"
    inlines = (
        ApplicantEducationInline,
        ResumeInline,
        PortfolioInline,
        PhoneInline,
    )
    fields = []

    list_display = ('id', 'get_fullname', 'get_status', 'date_created', 'get_link')
    list_filter = (YesterdayListFilter, 'sex')
    search_fields = ('last_name', 'first_name')

    '''
        TO BE REFACTORED !!!!
        NOW!!!!
    '''
    def get_status(self, obj):
        result_statuses = ''
        status = '<div><a target="_blank" href="/admin/vacancies/vacancy/%s">%s %s, %s</a> - %s</div><hr>'

        vacancy_statuses = ApplicantVacancyApplicantVacancyStatus.objects.filter(applicant_vacancy__applicant=obj).values(
                                                                            'applicant_vacancy__vacancy__id',
                                                                            'applicant_vacancy__vacancy__position__name',
                                                                            'applicant_vacancy__vacancy__head__name',
                                                                            'applicant_vacancy__vacancy__published_at',
                                                                            'applicant_vacancy_status__name')


        list_ids = []
        for vs in vacancy_statuses:
            vs_id = vs['applicant_vacancy__vacancy__id']

            if vs_id not in list_ids:
                for delete_vs in vacancy_statuses:
                    if vs_id == delete_vs['applicant_vacancy__vacancy__id']:
                        result = delete_vs

                list_ids.append(vs_id)
                result_statuses += status % (
                        result['applicant_vacancy__vacancy__id'],
                        result['applicant_vacancy__vacancy__head__name'],
                        result['applicant_vacancy__vacancy__position__name'],
                        datetime.strftime(result['applicant_vacancy__vacancy__published_at'], '%d-%m-%Y'),
                        result['applicant_vacancy_status__name']
                    )
                #return '<hr>' + result_statuses
        return result_statuses

    def get_fullname(self, obj):
        return '<a href="/admin/applicants/applicant/%s"><b>%s %s %s</b></a>' % (obj.id, obj.first_name, obj.last_name, obj.middle_name)

    def get_link(self, obj):
        return '<a target="_blank" href="/applicants/view/%s">Ссылка на страницу</a>' % (obj.id)

    get_status.short_description = 'Текущий статус'
    get_status.allow_tags = True

    get_fullname.short_description = 'ФИО'
    get_fullname.allow_tags = True

    get_link.short_description = 'Ссылка на страницу'
    get_link.allow_tags = True



class VacancyInline(BaseInline):
    model = Vacancy
    extra = 0


class PositionAdmin(BaseAdmin):
    inlines = (
        VacancyInline,
    )
    fields = ['name', 'author', 'date_created']
    list_display = ('id', 'get_name', 'get_author', 'date_created',)
    search_fields = ('name',)

    def get_name(self, obj):
        return '<a href="/admin/applicants/position/%s"><b>%s</b></a>' % (obj.id, obj.name)

    get_name.short_description = 'Должность'
    get_name.allow_tags = True

admin.site.register(Education, EducationAdmin)
admin.site.register(Major, MajorAdmin)
admin.site.register(SourceInformation, SourceAdmin)
admin.site.register(Applicant, ApplicantAdmin)
admin.site.register(Position, PositionAdmin)