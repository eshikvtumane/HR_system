from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import TemplateView
#from django.conf.urls.defaults import *

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'HR_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include('main.urls',namespace = 'main')),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^applicants/', include('applicants.urls', namespace='applicants')),
    url(r'^reports/', include('reports.urls', namespace='reports')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^vacancies/', include('vacancies.urls',namespace='vacancies')),
    url(r'^events/', include('events.urls',namespace='events')),
    url(r'^administration/', include('administration.urls', namespace='administration')),
    url(r'^email_constructor/', include('email_constructor.urls', namespace='email_constructor')),
    url(r'^notifications/', include('notifications.urls', namespace='notifications')),
    url(r'^employees/', include('employees.urls',namespace='employees'))
)

'''if not settings.DEBUG:
    urlpatterns += patterns(
        (r'404/$', TemplateView.as_view(template_name="404.html")),
        (r'500/$', TemplateView.as_view(template_name="500.html")),
    )'''
#http://stackoverflow.com/questions/16196603/images-from-imagefield-in-django-dont-load-in-templates
#https://docs.djangoproject.com/en/dev/howto/static-files/#deploying-static-files-in-a-nutshell
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)