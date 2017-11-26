from django.db import models
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from django_fsm import FSMField, transition
from djmoney.models.fields import MoneyField
from projects.models import *


class FundRequest(models.Model):
    class Statuses:
        NEW = 'NEW'
        APPROVED = 'APPROVED'
        REJECTED = 'REJECTED'
        CLOSED = 'CLOSED'

        @classmethod
        def choices(cls):
            return (
                (cls.NEW, _('New')),
                (cls.APPROVED, _('Approved')),
                (cls.REJECTED, _('Rejected')),
                (cls.CLOSED, _('Closed')),
            )

    amount = MoneyField(_('Amount'), null=True, blank=False,
                        decimal_places=2, default=0, default_currency='SAR', max_digits=11, )
    project = models.ForeignKey('projects.Project', related_name='requested_funds',
                                on_delete=models.SET_NULL, null=True, blank=True)
    justification = models.CharField(_('Justification'), null=True, blank=False, max_length=255)
    justification_proof = models.FileField(_('Justification Proof'), null=True, blank=True)
    requester = models.ForeignKey('projects.Employee', related_name='requested_funds',
                                  verbose_name=_('Requester'),
                                  on_delete=models.SET_NULL, null=True, blank=False)
    request_date = models.DateTimeField(_('Request Date'), null=True, blank=False)
    approval_status = FSMField(_('Approval Status'), default=Statuses.NEW,
                               choices=Statuses.choices())
    approved_amount = MoneyField(_('Approved Amount'), null=True, blank=True,
                                 decimal_places=2, default=0, default_currency='SAR', max_digits=11,)
    approved_by = models.ForeignKey('projects.Employee', related_name='approved_funds',
                                    verbose_name=_('Approved By'),
                                    on_delete=models.SET_NULL, null=True, blank=True)
    approval_comments = models.CharField(_('Approval Comments'), null=True, blank=True, max_length=255)
    approval_date = models.DateTimeField(_('Approval Date'), null=True, blank=True)
    created_on = models.DateTimeField(_('Created On'), auto_now_add=True)
    created_by = models.ForeignKey('projects.Employee', on_delete=models.SET_NULL, null=True, blank=False,
                                   verbose_name=_('Created By'),
                                   related_name="created_fund_requests", )
    updated_on = models.DateTimeField(_('Updated On'), auto_now=True)
    updated_by = models.ForeignKey('projects.Employee', on_delete=models.SET_NULL, null=True, blank=False,
                                   verbose_name=_('Updated By'))

    class Meta:
        verbose_name = _('Fund Request')
        verbose_name_plural = _('Fund Requests')

    @transition(field=approval_status, source=Statuses.NEW, target=Statuses.APPROVED)
    def approve(self):
        return

    @transition(field=approval_status, source=Statuses.NEW, target=Statuses.REJECTED)
    def reject(self):
        return

    @transition(field=approval_status, source=Statuses.NEW, target=Statuses.CLOSED)
    def close(self):
        return
    

class Invoice(models.Model):
    class Statuses:
        NEW = 'NEW'
        PENDING = 'PENDING'
        CLOSED = 'CLOSED'
        CANCELLED = 'CANCELLED'

        @classmethod
        def choices(cls):
            return (
                (cls.NEW, _('New')),
                (cls.PENDING, _('Pending')),
                (cls.CLOSED, _('Closed')),
                (cls.CANCELLED, _('Cancelled')),
            )

    reference = models.CharField(_('Invoice Reference'), null=True, blank=True, max_length=25)
    title_ar = models.CharField(_('Title'), max_length=100, blank=False, null=True)
    title_en = models.CharField(_('Title (English)'), max_length=100, blank=False, null=True)
    description_ar = models.TextField(_('Description'), null=True, blank=False)
    description_en = models.TextField(_('Description (English)'), null=True, blank=False)
    date = models.DateTimeField(_('Invoice Date'), null=True, blank=False)
    status = models.CharField(_('Handing Party Role'), max_length=20, null=True, blank=False,
                              choices=Statuses.choices())

    created_on = models.DateTimeField(_('Created On'), auto_now_add=True)
    created_by = models.ForeignKey('projects.Employee', on_delete=models.SET_NULL, null=True, blank=False,
                                   verbose_name=_('Created By'),
                                   related_name="created_invoices", )
    updated_on = models.DateTimeField(_('Updated On'), auto_now=True)
    updated_by = models.ForeignKey('projects.Employee', on_delete=models.SET_NULL, null=True, blank=False,
                                   verbose_name=_('Updated By'))


class Transaction(models.Model):
    class AccountingRoles:
        CLIENT = 'CLIENT'
        ACCOUNTING = 'ACCOUNTING'
        EMPLOYEE = 'EMPLOYEE'

        @classmethod
        def choices(cls):
            return (
                (cls.CLIENT, _('Client')),
                (cls.ACCOUNTING, _('Accounting')),
                (cls.EMPLOYEE, _('Employee')),
            )

    title_ar = models.CharField(_('Title'), max_length=100, blank=False, null=True)
    title_en = models.CharField(_('Title (English)'), max_length=100, blank=False, null=True)
    project = models.ForeignKey('projects.Project', related_name='transactions',
                                on_delete=models.SET_NULL, null=True, blank=True)
    amount = MoneyField(_('Amount'), null=True, blank=False,
                        decimal_places=2, default=0, default_currency='SAR', max_digits=11,)
    description_ar = models.CharField(_('Description'), null=True, blank=False, max_length=255)
    description_en = models.CharField(_('Description (English)'), null=True, blank=False, max_length=255)
    invoice = models.ForeignKey('Invoice', related_name='transactions',
                                on_delete=models.SET_NULL, null=True, blank=True)
    fund_request = models.ForeignKey('FundRequest', related_name='transactions',
                                     on_delete=models.SET_NULL, null=True, blank=True)
    handing_party = models.ForeignKey('projects.Person', related_name='handed_payments',
                                      verbose_name=_('Handing Party'),
                                      on_delete=models.SET_NULL, null=True, blank=False)
    handing_party_role = models.CharField(_('Handing Party Role'), max_length=20, null=True, blank=True,
                                          choices=AccountingRoles.choices())
    receiving_party = models.ForeignKey('projects.Person', related_name='received_payments',
                                        verbose_name=_('Receiving Party'),
                                        on_delete=models.SET_NULL, null=True, blank=False)
    receiving_party_role = models.CharField(_('Receiving Party Role'), max_length=20, null=True, blank=False,
                                            choices=AccountingRoles.choices())
    transaction_date = models.DateTimeField(_('Transaction Date'), null=True, blank=False)
    created_on = models.DateTimeField(_('Created On'), auto_now_add=True)
    created_by = models.ForeignKey('projects.Employee', on_delete=models.SET_NULL, null=True, blank=False,
                                   verbose_name=_('Created By'),
                                   related_name="created_transactions", )
    updated_on = models.DateTimeField(_('Updated On'), auto_now=True)
    updated_by = models.ForeignKey('projects.Employee', on_delete=models.SET_NULL, null=True, blank=False,
                                   verbose_name=_('Updated By'))

    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')

    def type(self):
        if self.handing_party_role == Transaction.AccountingRoles.ACCOUNTING \
                and self.receiving_party_role == Transaction.AccountingRoles.EMPLOYEE:
            if self.project:
                return _('Expenses')
            else:
                return _('Salaries')
        elif self.handing_party_role == Transaction.AccountingRoles.ACCOUNTING \
                and self.receiving_party_role == Transaction.AccountingRoles.CLIENT:
            return _('Returns to Client')
        elif self.handing_party_role == Transaction.AccountingRoles.CLIENT \
                and self.receiving_party_role == Transaction.AccountingRoles.ACCOUNTING:
            return _('Payments')
        elif self.handing_party_role == Transaction.AccountingRoles.EMPLOYEE \
                and self.receiving_party_role == Transaction.AccountingRoles.ACCOUNTING:
            return _('Returns on Expenses')
        else:
            return _('N/A')

    @property
    def title(self):
        lang = translation.get_language()
        if lang == "ar":
            return self.title_ar
        else:
            return self.title_en

    def __str__(self):
        return self.title

    @property
    def description(self):
        lang = translation.get_language()
        if lang == "ar":
            return self.description_ar
        else:
            return self.description_en
