import django_tables2 as tables
from django.utils.html import format_html

from django.utils.translation import ugettext_lazy as _

from .models import *


class DocumentMovementTable(tables.Table):

    class Meta:
        model = DocumentMovement
        fields = ['document', 'document.document', 'document.type', 'type', 'handing_party', 'receiving_party',
                  'movement_date', 'hard_copy', ]
        attrs = {'class': 'table table-striped table-bordered',
                 'id': 'datatable'}