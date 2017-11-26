from django.db import models
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from projects.models import *


class Document(models.Model):
    document = models.FileField(_('Document Upload'), null=True, blank=False)
    project = models.ForeignKey('projects.Project', related_name='documents',
                                on_delete=models.SET_NULL, null=True, blank=True)
    title_ar = models.CharField(_('Title'), max_length=100, blank=False, null=True)
    title_en = models.CharField(_('Title (English)'), max_length=100, blank=False, null=True)
    description = models.TextField(_('Description'), blank=False, null=True)
    description_en = models.TextField(_('Description (English)'), blank=False, null=True)
    type = models.CharField(_('Type'), max_length=100, null=True, blank=False,
                            choices=Lookup.get_lookup_choices(Lookup.LookupTypes.DOCUMENT_TYPE))
    uploaded_on = models.DateTimeField(_('Uploaded On'), auto_now_add=True)
    uploaded_by = models.ForeignKey('projects.Employee', on_delete=models.SET_NULL, null=True, blank=False,
                                    related_name='uploaded_documents',
                                    verbose_name=_('Uploaded By'))
    updated_on = models.DateTimeField(_('Updated On'), auto_now=True)
    updated_by = models.ForeignKey('projects.Employee', on_delete=models.SET_NULL, null=True, blank=False,
                                   # related_name='',
                                   verbose_name=_('Updated By'))

    class Meta:
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')

    @property
    def title(self):
        lang = translation.get_language()
        if lang == "ar":
            return self.title_ar
        else:
            return self.title_en

    def __str__(self):
        return self.title


class DocumentMovement(models.Model):
    class ArchiveRoles:
        CLIENT = 'CLIENT'
        ARCHIVE = 'ARCHIVE'
        EMPLOYEE = 'EMPLOYEE'

        @classmethod
        def choices(cls):
            return (
                (cls.CLIENT, _('Client')),
                (cls.ARCHIVE, _('Archive')),
                (cls.EMPLOYEE, _('Employee')),
            )

    document = models.ForeignKey('Document', related_name='movements',
                                 on_delete=models.CASCADE, null=False, blank=False)
    description = models.CharField(_('Description'), null=True, blank=False, max_length=255)
    hard_copy = models.BooleanField(_('Hard Copy Received?'), default=False)
    handing_party = models.ForeignKey('projects.Person', related_name='handed_documents',
                                      verbose_name=_('Handing Party'),
                                      on_delete=models.SET_NULL, null=True, blank=False)
    handing_party_role = models.CharField(_('Handing Party Role'), max_length=20, null=True, blank=True,
                                          choices=ArchiveRoles.choices())
    receiving_party = models.ForeignKey('projects.Person', related_name='received_documents',
                                        verbose_name=_('Receiving Party'),
                                        on_delete=models.SET_NULL, null=True, blank=False)
    receiving_party_role = models.CharField(_('Receiving Party Role'), max_length=20, null=True, blank=False,
                                            choices=ArchiveRoles.choices())
    movement_date = models.DateTimeField(_('Movement Date'), null=True, blank=False)

    class Meta:
        verbose_name = _('Document Movement')
        verbose_name_plural = _('Document Movements')

    def type(self):
        if self.handing_party_role == DocumentMovement.ArchiveRoles.ARCHIVE and self.receiving_party_role in (
                DocumentMovement.ArchiveRoles.EMPLOYEE, DocumentMovement.ArchiveRoles.CLIENT):
            return _('Outbox')
        elif self.receiving_party_role == DocumentMovement.ArchiveRoles.ARCHIVE and self.handing_party_role in (
                DocumentMovement.ArchiveRoles.EMPLOYEE,
                DocumentMovement.ArchiveRoles.CLIENT):
            return _('Inbox')
        else:
            return _('N/A')
