from crispy_forms.layout import Submit, Layout, ButtonHolder, Fieldset
from django import forms
from crispy_forms.helper import FormHelper
from django.utils import timezone

from django.utils.translation import ugettext_lazy as _

from .models import *
from.base_forms import *


class ProjectForm(BaseUpdatedByForm, forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title_ar', 'title_en', 'description', 'description_en', 'fees', 'main_assignee']


class CaseForm(ProjectForm):
    class Meta:
        model = Case
        fields = ProjectForm.Meta.fields + ['type', 'case_reference', 'client', 'client_role',
                                            'opponent', 'opponent_role', 'court', 'court_office']

    def __init__(self, *args, **kwargs):
        super(CaseForm, self).__init__(*args, **kwargs)


class PaperworkForm(ProjectForm):
    class Meta:
        model = Paperwork
        fields = ProjectForm.Meta.fields + ['type', 'client', ]

    def __init__(self, *args, **kwargs):
        super(PaperworkForm, self).__init__(*args, **kwargs)


class ConsultationForm(ProjectForm):
    class Meta:
        model = Consultation
        fields = ProjectForm.Meta.fields + ['type', 'client', ]

    def __init__(self, *args, **kwargs):
        super(ConsultationForm, self).__init__(*args, **kwargs)


class NewUpdateForm(BaseUpdatedByForm, forms.ModelForm):
    class Meta:
        model = Update
        fields = ['summary_ar', 'summary_en', 'details_ar', 'details_en', 'date', 'attachments', 'inform_the_client']

    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project')
        super(NewUpdateForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(NewUpdateForm, self).save(commit=False)
        instance.project = self.project
        instance.created_on = timezone.now()
        instance.created_by = self.employee

        if commit:
            instance.save()

        return instance
