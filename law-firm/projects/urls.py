from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^listing/(?P<p_type>\w+)/$', views.ProjectListing.as_view(), name='case_listing'),
    url(r'^project/(?P<p_type>\w+)/$', views.NewProjectView.as_view(), name='new_project'),
    url(r'^update_project/(?P<pk>\d+)/$', views.UpdateProjectView.as_view(), name='update_project'),
    url(r'^project/(?P<pk>\d+)/update/$', views.NewUpdateView.as_view(), name='new_update'),
    url(r'^project/(?P<pk>\d+)/request_fund/$', views.NewFundRequestView.as_view(), name='new_request_fund'),

    url(r'^clients/$', views.ClientListing.as_view(), name='clients'),
    url(r'^client/$', views.NewClientView.as_view(), name='new_client'),
    url(r'^client/(?P<pk>\d+)/$', views.ClientView.as_view(), name='update_client'),

    url(r'^organizations/$', views.OrganizationListing.as_view(), name='organizations'),
    url(r'^organization/$', views.NewOrganizationView.as_view(), name='new_organization'),
    url(r'^organization/(?P<pk>\d+)/$', views.OrganizationView.as_view(), name='update_organization'),
]

