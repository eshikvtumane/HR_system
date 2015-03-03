from django.conf.urls import patterns, include, url
from views import MainPageView


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'HR_project.vSiews.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', MainPageView.as_view()),
    #url(r'^admin/', include(admin.site.urls)),
)