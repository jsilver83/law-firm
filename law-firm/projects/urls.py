from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^listing/(?P<p_type>\w+)/$', views.ProjectListing.as_view(), name='case_listing'),
    url(r'^project/(?P<p_type>\w+)/$', views.NewProjectView.as_view(), name='new_project'),
    url(r'^update_project/(?P<pk>\d+)/$', views.UpdateProjectView.as_view(), name='update_project'),
    url(r'^project/(?P<pk>\d+)/request_fund$', views.NewFundRequestView.as_view(), name='request_fund'),
    url(r'^project/(?P<pk>\d+)/update$', views.NewUpdateView.as_view(), name='new_update'),
]
