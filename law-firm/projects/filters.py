import django_filters as filters
from dal import autocomplete
from django.db.models import Q

from django.utils.translation import ugettext_lazy as _

from .models import *


class ProjectFilter(filters.FilterSet):
    general_search = filters.CharFilter(method='custom_title_filter', label=_('Title (Arabic or English)'))

    class Meta:
        model = Project
        fields = {
            'status': ['exact'],
            'client': ['exact'],
        }

    def custom_title_filter(self, queryset, name, value):
        return queryset.filter(Q(title_ar__icontains=value) | Q(title_en__icontains=value))

    def __init__(self, *args, **kwargs):
        super(ProjectFilter, self).__init__(*args, **kwargs)
        self.filters['client'].widget = autocomplete.ModelSelect2(url='client-autocomplete', )


class CaseFilter(ProjectFilter):
    class Meta:
        model = Case
        fields = {
            'status': ['exact'],
            'client': ['exact'],
            'case_reference': ['icontains'],
        }

    def __init__(self, *args, **kwargs):
        super(CaseFilter, self).__init__(*args, **kwargs)
        self.filters['case_reference__icontains'].label = _('Case Reference')


class ClientFilter(filters.FilterSet):
    general_search = filters.CharFilter(method='custom_name_filter', label=_('Name (Arabic or English)'))

    class Meta:
        model = Client
        fields = {
            'organization': ['exact', 'isnull'],
        }

    def custom_name_filter(self, queryset, name, value):
        return queryset.filter(Q(name_ar__icontains=value) | Q(name_en__icontains=value))

    def __init__(self, *args, **kwargs):
        super(ClientFilter, self).__init__(*args, **kwargs)
        self.filters['organization__isnull'].label = _('Individuals')


class OrganizationFilter(filters.FilterSet):
    general_search = filters.CharFilter(method='custom_name_filter', label=_('Name (Arabic or English)'))
    city = filters.AllValuesFilter()

    class Meta:
        model = Organization
        fields = {
            # 'city': ['icontains'],
            'type': ['exact'],
        }

    def custom_name_filter(self, queryset, name, value):
        return queryset.filter(Q(name_ar__icontains=value) | Q(name_en__icontains=value))


class EmployeeFilter(filters.FilterSet):
    general_search = filters.CharFilter(method='custom_name_filter', label=_('Name (Arabic or English)'))
    job_description = filters.CharFilter(method='custom_job_filter', label=_('Job Description'))

    class Meta:
        model = Employee
        fields = {
            'mobile': ['icontains'],
            'nationality': ['exact'],
        }

    def custom_name_filter(self, queryset, name, value):
        return queryset.filter(Q(name_ar__icontains=value) | Q(name_en__icontains=value))

    def custom_job_filter(self, queryset, name, value):
        return queryset.filter(Q(job_description_ar__icontains=value) | Q(job_description_en__icontains=value))
