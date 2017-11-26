import django_tables2 as tables
from django.utils.html import format_html

from django.utils.translation import ugettext_lazy as _

from .models import *


class FundRequestTable(tables.Table):

    class Meta:
        model = FundRequest
        fields = ['requester', 'amount', 'justification', 'request_date', 'approval_status', 'approved_amount',
                  'approved_by', 'approval_comments', 'approval_date', ]
        attrs = {'class': 'table table-striped table-bordered',
                 'id': 'datatable'}