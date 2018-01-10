from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy, reverse
from django.utils.html import format_html
from django.views.generic import TemplateView, UpdateView, CreateView, FormView
from django.utils.translation import ugettext_lazy as _
from django_filters.views import FilterView
from django_tables2 import SingleTableView, MultiTableMixin, SingleTableMixin

from .models import *
from .forms import *
from .tables import *
from .filters import ProjectFilter, CaseFilter, ClientFilter, OrganizationFilter
from accounting.forms import NewFundRequestForm
from archive.models import DocumentMovement
from archive.tables import DocumentMovementTable
from accounting.tables import *


class BaseLawyerView(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        print(self.request.user.groups)
        return self.request.user.groups.filter(name__in=['Admins', 'Lawyers']).exists() \
               or self.request.user.is_superuser


class Index(TemplateView):
    template_name = 'projects/index.html'


class ProjectListing(BaseLawyerView, SingleTableMixin, FilterView):
    model = Case
    table_pagination = {
        'per_page': 10
    }
    template_name = 'projects/projects_listing.html'

    def get_queryset(self):
        p_type = self.kwargs['p_type']

        if p_type.lower() == 'case':
            self.model = Case
        elif p_type.lower() == 'paperwork':
            self.model = Paperwork
        else:
            self.model = Consultation

        if self.request.user.is_superuser:
            return self.model.objects.all()
        else:
            employee, s = Employee.objects.get_or_create(user=self.request.user)
            return self.model.objects.filter(main_assignee=employee)

    def get_table_class(self):
        p_type = self.kwargs['p_type']

        if p_type.lower() == 'case':
            return CaseTable
        elif p_type.lower() == 'paperwork':
            return ProjectTable
        else:
            return ProjectTable

    def get_table_kwargs(self):
        kwargs = super(ProjectListing, self).get_table_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ProjectListing, self).get_context_data(**kwargs)

        p_type = self.kwargs['p_type']

        context['p_type'] = p_type

        if p_type.lower() == 'case':
            context['header_title'] = _('Cases')
            context['new_project_text'] = _('New Case')
        elif p_type.lower() == 'paperwork':
            context['header_title'] = _('Paperwork Projects')
            context['new_project_text'] = _('New Paperwork Project')
        else:
            context['header_title'] = _('Consultations')
            context['new_project_text'] = _('New Consultation')

        context['search_form'] = BaseCrispySearchForm

        return context

    def get_filterset_class(self):
        p_type = self.kwargs['p_type']

        if p_type.lower() == 'case':
            return CaseFilter
        elif p_type.lower() == 'paperwork':
            return ProjectFilter
        else:
            return ProjectFilter


class BaseFormView(object):

    def get_form_kwargs(self):
        kwargs = super(BaseFormView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class NewProjectView(SuccessMessageMixin, BaseLawyerView, BaseFormView, CreateView):
    # model = Case
    # form_class = CaseForm
    template_name = 'projects/new-project.html'
    success_message = _('Project was created successfully')
    # success_url = reverse_lazy('case_listing')

    def get_form_class(self):
        p_type = self.kwargs['p_type']

        if p_type.lower() == 'case':
            return CaseForm
        elif p_type.lower() == 'paperwork':
            return PaperworkForm
        else:
            return ConsultationForm

    def form_valid(self, form):
        employee, created = Employee.objects.get_or_create(user=self.request.user)
        instance = form.save(commit=False)
        instance.created_by = employee
        self.success_url = reverse_lazy('case_listing', args=(type(instance).__name__, ))
        return super(NewProjectView, self).form_valid(form)


class UpdateProjectView(SuccessMessageMixin, MultiTableMixin, BaseLawyerView, BaseFormView, UpdateView):
    template_name = 'projects/update-project.html'
    success_message = _('Project was updated successfully')

    # TODO: remove the ugly nested try ... excepts
    def get_object(self, queryset=None):
        try:
            project = Project.objects.get(pk=self.kwargs['pk'])

            try:
                if hasattr(project.case, 'pk'):
                    return project.case
            except Case.DoesNotExist:
                try:
                    if hasattr(project.consultation, 'pk'):
                        return project.consultation
                except Consultation.DoesNotExist:
                    try:
                        if hasattr(project.paperwork, 'pk'):
                            return project.paperwork
                    except Paperwork.DoesNotExist:
                        pass
        except Project.DoesNotExist:
            pass

    def get_success_url(self):
        return reverse_lazy('case_listing', args=(type(self.object).__name__, ))

    def get_form_class(self):
        if isinstance(self.object, Case):
            return CaseForm
        else:
            return ProjectForm

    def get_tables(self):
        fund_requests = FundRequest.objects.filter(project=self.get_object())
        docs_movements = DocumentMovement.objects.filter(document__project=self.get_object())
        invoices = Invoice.objects.filter(project=self.get_object())
        employee, d = Employee.objects.get_or_create(user=self.request.user)
        reminders = Reminder.objects.filter(project=self.get_object(),
                                            whom_to_remind=employee)
        return [
            FundRequestTable(fund_requests, user=self.request.user),
            DocumentMovementTable(docs_movements, user=self.request.user),
            InvoiceTable(invoices, user=self.request.user),
            ReminderTable(reminders, user=self.request.user, project_page=True),
        ]

    # TODO: implement case ownership check
    def test_func(self):
        return super(UpdateProjectView, self).test_func()


class NewFundRequestView(SuccessMessageMixin, BaseLawyerView, BaseFormView, CreateView):
    form_class = NewFundRequestForm
    template_name = 'projects/new-project.html'
    success_message = _('Fund request was submitted successfully. Check later for approval status')

    def get_form_kwargs(self):
        kwargs = super(NewFundRequestView, self).get_form_kwargs()
        kwargs['project'] = Project.objects.get(pk=self.kwargs['pk'])
        return kwargs

    def get_success_url(self):
        return reverse_lazy('update_project', args=(self.kwargs['pk'], ))


class NewUpdateView(SuccessMessageMixin, BaseLawyerView, BaseFormView, CreateView):
    form_class = NewUpdateForm
    template_name = 'projects/new-project.html'
    success_message = _('Update was submitted successfully.')

    def get_form_kwargs(self):
        kwargs = super(NewUpdateView, self).get_form_kwargs()
        kwargs['project'] = Project.objects.get(pk=self.kwargs['pk'])
        return kwargs

    def get_success_url(self):
        return reverse_lazy('update_project', args=(self.kwargs['pk'], ))


class ClientListing(BaseLawyerView, SingleTableMixin, FilterView):
    model = Case
    table_class = ClientTable
    table_pagination = {
        'per_page': 10
    }
    filterset_class = ClientFilter
    template_name = 'projects/clients_listing.html'

    def get_queryset(self):
        return Client.objects.all()

    # def get_table(self):
    #     return self.table_class(self.get_queryset() , user=self.request.user)

    def get_table_kwargs(self):
        kwargs = super(ClientListing, self).get_table_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ClientListing, self).get_context_data(**kwargs)

        context['search_form'] = BaseCrispySearchForm

        return context


class ClientView(SuccessMessageMixin, BaseLawyerView, BaseFormView, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'projects/form.html'
    success_url = reverse_lazy('clients')
    success_message = _('Client info was updated successfully')


class NewClientView(BaseLawyerView, BaseFormView, CreateView):
    form_class = ClientForm
    template_name = 'projects/form.html'
    success_url = reverse_lazy('clients')
    success_message = _('Client was added successfully')


class OrganizationListing(BaseLawyerView, SingleTableMixin, FilterView):
    model = Organization
    table_class = OrganizationTable
    table_pagination = {
        'per_page': 10
    }
    filterset_class = OrganizationFilter
    template_name = 'projects/organizations_listing.html'

    def get_queryset(self):
        return Organization.objects.all()

    def get_table_kwargs(self):
        kwargs = super(OrganizationListing, self).get_table_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(OrganizationListing, self).get_context_data(**kwargs)

        context['search_form'] = BaseCrispySearchForm

        return context


class OrganizationView(SuccessMessageMixin, BaseLawyerView, BaseFormView, UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'projects/form.html'
    success_url = reverse_lazy('organizations')
    success_message = _('Organization info was updated successfully')


class NewOrganizationView(BaseLawyerView, BaseFormView, CreateView):
    form_class = OrganizationForm
    template_name = 'projects/form.html'
    success_url = reverse_lazy('clients')
    success_message = _('Organization was added successfully')


class NewReminderView(SuccessMessageMixin, BaseLawyerView, BaseFormView, CreateView):
    form_class = NewReminderForm
    template_name = 'projects/form.html'
    success_message = _('Reminder was created successfully.')

    def get_form_kwargs(self):
        kwargs = super(NewReminderView, self).get_form_kwargs()
        kwargs['project'] = Project.objects.get(pk=self.kwargs['pk'])
        return kwargs

    def get_success_url(self):
        return reverse_lazy('update_project', args=(self.kwargs['pk'], ))
