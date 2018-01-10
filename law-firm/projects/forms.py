from crispy_forms.layout import Submit, Layout, ButtonHolder, Fieldset
from django import forms
from crispy_forms.helper import FormHelper
from django.utils import timezone
from dal import autocomplete

from django.utils.translation import ugettext_lazy as _

from .models import *
from.base_forms import *


class ProjectForm(BaseUpdatedByForm, forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title_ar', 'title_en', 'description_ar', 'description_en', 'fees', 'main_assignee']


class CaseForm(ProjectForm):
    class Meta:
        model = Case
        fields = ProjectForm.Meta.fields + ['type', 'case_reference', 'client', 'client_role',
                                            'opponent', 'opponent_role', 'court', 'court_office']
        widgets = {
            'client': autocomplete.ModelSelect2(url='client-autocomplete',
                                                # add_another_url_name='client_add_another_model_create'
                                                ),
            'opponent': autocomplete.ModelSelect2(url='client-autocomplete', ),
            'court': autocomplete.ModelSelect2(url='court-autocomplete', ),
        }

    def __init__(self, *args, **kwargs):
        super(CaseForm, self).__init__(*args, **kwargs)


class PaperworkForm(ProjectForm):
    class Meta:
        model = Paperwork
        fields = ProjectForm.Meta.fields + ['type', 'client', ]
        widgets = {
            'client': autocomplete.ModelSelect2(url='client-autocomplete', ),
        }

    def __init__(self, *args, **kwargs):
        super(PaperworkForm, self).__init__(*args, **kwargs)


class ConsultationForm(ProjectForm):
    class Meta:
        model = Consultation
        fields = ProjectForm.Meta.fields + ['type', 'client', ]
        widgets = {
            'client': autocomplete.ModelSelect2(url='client-autocomplete', ),
        }

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


class ClientForm(BaseUpdatedByForm, forms.ModelForm):
    class Meta:
        model = Client
        fields = ['organization', 'name_ar', 'name_en', 'mobile', 'home_phone', 'work_phone', 'personal_email',
                  'government_id', 'gender', 'nationality', 'date_of_birth', 'address', 'active', 'personal_picture', ]
        help_texts = {
            'organization': _('Choose from the above list if this client belongs to an organization. If the name of '
                              'the organization does NOT appear in the list, you need to add it first and '
                              'come back here')
        }
        widgets = {
            'organization': autocomplete.ModelSelect2(url='org-autocomplete', ),
            'nationality': autocomplete.ModelSelect2(url='nationality-autocomplete', ),
        }


class OrganizationForm(BaseUpdatedByForm, forms.ModelForm):
    class Meta:
        model = Organization
        fields = '__all__'
        exclude = ['created_by', 'created_on', 'updated_by', 'updated_on']


class NewReminderForm(BaseUpdatedByForm, forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['title_ar', 'title_en', 'description_ar', 'description_en', 'date', 'type']

    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project')
        super(NewReminderForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(NewReminderForm, self).save(commit=False)
        instance.project = self.project
        instance.whom_to_remind = self.employee

        if commit:
            instance.save()

        return instance
