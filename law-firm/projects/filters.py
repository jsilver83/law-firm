import django_filters as filters
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
