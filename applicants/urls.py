from django.conf.urls import patterns, include, url
from views import ApplicantAddView


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'HR_project.vSiews.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^add/$', ApplicantAddView.as_view(), name='applicant_add'),
    #url(r'^admin/', include(admin.site.urls)),
)