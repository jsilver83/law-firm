from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.html import format_html
from django.views.generic import TemplateView, UpdateView, CreateView, FormView
from django.utils.translation import ugettext_lazy as _
from django_filters.views import FilterView
from django_tables2 import SingleTableView, MultiTableMixin, SingleTableMixin

from projects.base_forms import BaseCrispySearchForm
from archive.filters import DocumentMovementFilter
from projects.views import BaseFormView
from .models import *
from .forms import *
from .tables import *
from .filters import *


class BaseAccountingView(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name__in=['Admins', 'Accounting']).exists() \
               or self.request.user.is_superuser


class InvoiceListing(BaseAccountingView, SingleTableMixin, FilterView):
    model = Invoice
    table_class = InvoiceTable
    table_pagination = {
        'per_page': 10
    }
    filterset_class = InvoiceFilter
    template_name = 'accounting/invoice_listing.html'

    def get_queryset(self):
        return Invoice.objects.all()

    # def get_table(self):
    #     return self.table_class(self.get_queryset() , user=self.request.user)

    def get_table_kwargs(self):
        kwargs = super(InvoiceListing, self).get_table_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(InvoiceListing, self).get_context_data(**kwargs)

        context['search_form'] = BaseCrispySearchForm

        return context


class UpdateInvoiceView(SuccessMessageMixin, BaseAccountingView, BaseFormView, UpdateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'projects/form.html'
    success_url = reverse_lazy('invoice_listing')
    success_message = _('Invoice info was updated successfully')


class NewInvoiceView(BaseAccountingView, BaseFormView, CreateView):
    form_class = NewInvoiceForm
    template_name = 'projects/form.html'
    success_url = reverse_lazy('invoice_listing')
    success_message = _('Invoice was added successfully')

    def get_form_kwargs(self):
        kwargs = super(NewInvoiceView, self).get_form_kwargs()
        if 'project_pk' in self.kwargs:
            kwargs['project'] = self.kwargs['project_pk']
        return kwargs


class FundRequestListing(BaseAccountingView, SingleTableMixin, FilterView):
    model = FundRequest
    table_class = FundRequestTable
    table_pagination = {
        'per_page': 10
    }
    filterset_class = FundRequestFilter
    template_name = 'accounting/fund_request_listing.html'

    def get_queryset(self):
        return FundRequest.objects.all()

    def get_table_kwargs(self):
        kwargs = super(FundRequestListing, self).get_table_kwargs()
        kwargs['user'] = self.request.user
        kwargs['accounting'] = True
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(FundRequestListing, self).get_context_data(**kwargs)

        context['search_form'] = BaseCrispySearchForm

        return context


class FundRequestApprovalView(SuccessMessageMixin, BaseAccountingView, BaseFormView, UpdateView):
    model = FundRequest
    form_class = ApproveFundRequestForm
    template_name = 'accounting/approve_fund_request.html'
    success_message = _('Fund request was updated successfully.')

    def get_success_url(self):
        return reverse_lazy('fund_request_listing')


class NewExpenseView(SuccessMessageMixin, BaseAccountingView, BaseFormView, CreateView):
    form_class = NewExpenseForm
    template_name = 'accounting/new_expense.html'
    success_url = reverse_lazy('fund_request_listing')
    success_message = _('Expense was added successfully')

    def get_form_kwargs(self):
        kwargs = super(NewExpenseView, self).get_form_kwargs()
        kwargs['fund_request_pk'] = self.kwargs['fund_request_pk']
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(NewExpenseView, self).get_context_data(**kwargs)
        context['object'] = get_object_or_404(FundRequest, pk=self.kwargs['fund_request_pk'])
        return context


class NewPaymentView(SuccessMessageMixin, BaseAccountingView, BaseFormView, CreateView):
    form_class = NewPaymentForm
    template_name = 'accounting/new_payment.html'
    success_url = reverse_lazy('invoice_listing')
    success_message = _('Payment was added successfully')

    def get_form_kwargs(self):
        kwargs = super(NewPaymentView, self).get_form_kwargs()
        kwargs['invoice_pk'] = self.kwargs['invoice_pk']
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(NewPaymentView, self).get_context_data(**kwargs)
        context['object'] = get_object_or_404(Invoice, pk=self.kwargs['invoice_pk'])
        return context


class TransactionListing(BaseAccountingView, SingleTableMixin, FilterView):
    model = Transaction
    table_class = TransactionTable
    table_pagination = {
        'per_page': 10
    }
    filterset_class = TransactionFilter
    template_name = 'accounting/transaction_listing.html'

    def get_queryset(self):
        return Transaction.objects.all()

    def get_table_kwargs(self):
        kwargs = super(TransactionListing, self).get_table_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(TransactionListing, self).get_context_data(**kwargs)

        context['search_form'] = BaseCrispySearchForm

        return context

