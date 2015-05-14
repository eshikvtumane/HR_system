from django.conf.urls import patterns, include, url
from views import MainPageView, GlobalSearchView, TodoDeleteAjax


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'HR_project.vSiews.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', MainPageView.as_view(), name="main_page"),
    url(r'^global_search/$', GlobalSearchView.as_view(), name="global_search"),
    url(r'^todo_delete/(?P<record_id>[0-9]+)/$', TodoDeleteAjax.as_view(), name="todo_delete"),
    #url(r'^admin/', include(admin.site.urls)),
)