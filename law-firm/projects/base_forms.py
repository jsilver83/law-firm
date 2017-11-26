from crispy_forms.layout import Submit, Layout, ButtonHolder, Fieldset
from crispy_forms.helper import FormHelper

from django.utils.translation import ugettext_lazy as _

from .models import Employee


class BaseCrispyForm:

    def __init__(self, *args, **kwargs):
        super(BaseCrispyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal form-label-left'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-7'


class BaseCrispySearchForm(BaseCrispyForm):

    def __init__(self, *args, **kwargs):
        super(BaseCrispySearchForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('search', _('Search')))
        self.helper.form_method = 'get'


class BaseUpdatedByForm(BaseCrispyForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.employee, created = Employee.objects.get_or_create(user=self.user)
        super(BaseUpdatedByForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', _('Submit')))

    def save(self, commit=True):
        instance = super(BaseUpdatedByForm, self).save(commit=False)
        instance.updated_by = self.employee
        if commit:
            instance.save()
        return instance
