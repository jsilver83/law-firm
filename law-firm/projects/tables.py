import django_tables2 as tables
from django.utils.html import format_html

from django.utils.translation import ugettext_lazy as _

from .models import *


class BaseTableWithCommands(tables.Table):
    view_link = tables.TemplateColumn('{{ html }}', orderable=False, verbose_name='')
    update_link = tables.TemplateColumn('{{ html }}', orderable=False, verbose_name='')
    delete_link = tables.TemplateColumn('{{ html }}', orderable=False, verbose_name='')

    def render_view_link(self, *args, **kwargs):
        record = kwargs.pop('record')
        commands = '<a href="%s" class="btn btn-primary btn-xs"><i class="fa fa-folder"></i> %s</a>' \
                   % (record.get_absolute_url(), _('View'))
        return format_html(commands)

    def render_update_link(self, *args, **kwargs):
        record = kwargs.pop('record')
        commands = '<a href="%s" class="btn btn-info btn-xs"><i class="fa fa-pencil"></i> %s</a>' \
                   % (record.get_update_url(), _('Edit'))
        return format_html(commands)

    def render_delete_link(self, *args, **kwargs):
        record = kwargs.pop('record')
        commands = '<a href="%s" class="btn btn-danger btn-xs"><i class="fa fa-trash-o"></i> %s</a>' \
                   % (record.get_absolute_url(), _('Delete'))
        return format_html(commands)

    def __init__(self, *args, **kwargs):
        self.employee, d = Employee.objects.get_or_create(user=kwargs.pop('user'))
        super(BaseTableWithCommands, self).__init__(*args, **kwargs)

        self.exclude = ()
        if not self.can_view():
            self.exclude = self.exclude + ('view_link', )

        if not self.can_update():
            self.exclude = self.exclude + ('update_link', )

        if not self.can_delete():
            self.exclude = self.exclude + ('delete_link', )

    def can_view(self):
        return False

    def can_update(self):
        return False

    def can_delete(self):
        return False


class ProjectTable(BaseTableWithCommands):

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

    class Meta:
        model = Project
        fields = ['title', 'status', 'main_assignee', 'client', ]
        exclude = ['id']
        attrs = {'class': 'table table-striped table-bordered', }


class ClientTable(BaseTableWithCommands):
    personal_email = tables.EmailColumn()
    # organization = tables.RelatedLinkColumn()

    class Meta:
        model = Project
        fields = ['name', 'organization', 'mobile', 'work_phone', 'personal_email', 'gender', 'nationality']
        attrs = {'class': 'table table-striped table-bordered', }

    def order_name(self, queryset, is_descending):
        lang = translation.get_language()
        if lang == "ar":
            queryset = queryset.order_by(('-' if is_descending else '') + 'name_ar')
        else:
            queryset = queryset.order_by(('-' if is_descending else '') + 'name_en')
        return queryset, True


class OrganizationTable(BaseTableWithCommands):

    class Meta:
        model = Project
        fields = ['name', 'type', 'phone', 'website', 'city', ]
        attrs = {'class': 'table table-striped table-bordered', }

    def order_name(self, queryset, is_descending):
        lang = translation.get_language()
        if lang == "ar":
            queryset = queryset.order_by(('-' if is_descending else '') + 'name_ar')
        else:
            queryset = queryset.order_by(('-' if is_descending else '') + 'name_en')
        return queryset, True

