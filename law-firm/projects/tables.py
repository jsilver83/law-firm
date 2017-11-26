import django_tables2 as tables
from django.utils.html import format_html

from django.utils.translation import ugettext_lazy as _

from .models import *


class ProjectTable(tables.Table):
    commands = tables.TemplateColumn('{{ html }}', orderable=False)
    title = tables.Column(accessor='title')

    class Meta:
        model = Project
        fields = ['title', 'status', 'main_assignee', 'client', ]
        exclude = ['id']
        attrs = {'class': 'table table-striped table-bordered',
                 # 'id': 'datatable',
                 }

    def render_client(self, value):
        if value.client.organization:
            return format_html('%s<br><small>%s</small>' % (value.client, value.client.organization))
        else:
            return value.client

    def render_commands(self, *args, **kwargs):
        record = kwargs.pop('record')

        commands = '<a href="%s" target="_blank">%s</a>' % (record.get_update_url(), _('Edit'))

        if record.status == Project.Statuses.NEW:
            pass
        return format_html(commands)

    def order_title(self, queryset, is_descending):
        lang = translation.get_language()
        if lang == "ar":
            queryset = queryset.order_by(('-' if is_descending else '') + 'title_ar')
        else:
            queryset = queryset.order_by(('-' if is_descending else '') + 'title_en')
        return queryset, True

    # def __init__(self, *args, **kwargs):
    #     super(ProjectTable, self).__init__(*args, **kwargs)
        # self.columns['title'].orderable = False


class CaseTable(ProjectTable):
    class Meta(ProjectTable.Meta):
        fields = ProjectTable.Meta.fields + ['client_role', 'type', 'case_reference', 'court', 'updated_on']


class ReminderTable(tables.Table):
    commands = tables.TemplateColumn('{{ html }}', orderable=False)

    class Meta:
        model = Project
        fields = ['title', 'status', 'main_assignee', 'client', ]
        exclude = ['id']
        attrs = {'class': 'table table-striped table-bordered',
                 'id': 'datatable'}
