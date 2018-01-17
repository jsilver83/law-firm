from django.conf.urls import url

from . import auto_complete_views
from . import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),

    url(r'^listing/(?P<p_type>\w+)/$', views.ProjectListing.as_view(), name='case_listing'),
    url(r'^project/(?P<p_type>\w+)/$', views.NewProjectView.as_view(), name='new_project'),
    url(r'^update_project/(?P<pk>\d+)/$', views.UpdateProjectView.as_view(), name='update_project'),
    url(r'^project/(?P<pk>\d+)/update/$', views.NewUpdateView.as_view(), name='new_update'),
    url(r'^project/(?P<pk>\d+)/request_fund/$', views.NewFundRequestView.as_view(), name='new_request_fund'),
    url(r'^project/(?P<pk>\d+)/reminder/$', views.NewReminderView.as_view(), name='new_project_reminder'),

    url(r'^clients/$', views.ClientListing.as_view(), name='clients'),
    url(r'^client/$', views.NewClientView.as_view(), name='new_client'),
    url(r'^client/(?P<pk>\d+)/$', views.ClientView.as_view(), name='update_client'),

    url(r'^organizations/$', views.OrganizationListing.as_view(), name='organizations'),
    url(r'^organization/$', views.NewOrganizationView.as_view(), name='new_organization'),
    url(r'^organization/(?P<pk>\d+)/$', views.OrganizationView.as_view(), name='update_organization'),

    url(r'^employees/$', views.EmployeesListing.as_view(), name='employees'),
    url(r'^employee/$', views.NewEmployeeView.as_view(), name='new_employee'),
    url(r'^employee/(?P<pk>\d+)/$', views.EmployeeView.as_view(), name='update_employee'),
    url(r'^new-user/$', views.NewUserView.as_view(), name='new-user'),
    url(r'^user/(?P<pk>\d+)/$', views.ChangeUserView.as_view(), name='change-user'),

    url(r'^client-autocomplete/$', auto_complete_views.ClientAutocomplete.as_view(), name='client-autocomplete', ),
    url(r'^org-autocomplete/$', auto_complete_views.OrganizationAutocomplete.as_view(), name='org-autocomplete', ),
    url(r'^court-autocomplete/$', auto_complete_views.CourtAutocomplete.as_view(), name='court-autocomplete', ),
    url(r'^nationality-autocomplete/$',
        auto_complete_views.NationalityAutocomplete.as_view(),
        name='nationality-autocomplete', ),

    # url(r'$', al.CreateView.as_view(
    #     model=Client, form_class=ClientForm),
    #     name='client_add_another_model_create'),
]

