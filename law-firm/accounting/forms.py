from crispy_forms.layout import Submit, Layout, ButtonHolder, Fieldset
from django import forms
from crispy_forms.helper import FormHelper
from django.utils import timezone

from django.utils.translation import ugettext_lazy as _

from projects.base_forms import BaseUpdatedByForm
from .models import *


class NewFundRequestForm(BaseUpdatedByForm, forms.ModelForm):
    class Meta:
        model = FundRequest
        fields = ['amount', 'justification', 'justification_proof']

    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project')
        super(NewFundRequestForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(NewFundRequestForm, self).save(commit=False)
        instance.project = self.project
        instance.requester = self.employee
        instance.request_date = timezone.now()
        instance.created_on = timezone.now()
        instance.created_by = self.employee

        if commit:
            instance.save()

        return instance
