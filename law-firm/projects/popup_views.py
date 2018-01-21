from django.views.generic import CreateView, UpdateView
from django_addanother.views import CreatePopupMixin, UpdatePopupMixin

from .views import NewOrganizationView, BaseFormView
from .forms import MyUserCreationForm, MyUserChangeForm, OrganizationForm, NationalityForm, ClientForm, CourtForm


class NewUserView(CreatePopupMixin, CreateView):
    form_class = MyUserCreationForm
    template_name = 'projects/plain-form.html'


class ChangeUserView(UpdatePopupMixin, UpdateView):
    form_class = MyUserChangeForm
    template_name = 'projects/plain-form.html'


class NewClientPopupView(CreatePopupMixin, BaseFormView, CreateView):
    form_class = ClientForm
    template_name = 'projects/plain-form.html'


class NewOrganizationPopupView(CreatePopupMixin, BaseFormView, CreateView):
    form_class = OrganizationForm
    template_name = 'projects/plain-form.html'


class NewCourtPopupView(CreatePopupMixin, BaseFormView, CreateView):
    form_class = CourtForm
    template_name = 'projects/plain-form.html'


class NewNationalityPopupView(CreatePopupMixin, BaseFormView, CreateView):
    form_class = NationalityForm
    template_name = 'projects/plain-form.html'
