from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from django_addanother.views import CreatePopupMixin, UpdatePopupMixin

from .views import NewOrganizationView, BaseFormView, BaseAdminView, BaseLawyerView
from .forms import MyUserCreationForm, MyUserChangeForm, OrganizationForm, NationalityForm, ClientForm, CourtForm


class NewUserView(BaseAdminView, CreatePopupMixin, CreateView):
    form_class = MyUserCreationForm
    template_name = 'projects/plain-form.html'


class ChangeUserView(BaseAdminView, UpdatePopupMixin, UpdateView):
    form_class = MyUserChangeForm
    template_name = 'projects/plain-form.html'


class NewClientPopupView(LoginRequiredMixin, CreatePopupMixin, BaseFormView, CreateView):
    form_class = ClientForm
    template_name = 'projects/plain-form.html'


class NewOrganizationPopupView(LoginRequiredMixin, CreatePopupMixin, BaseFormView, CreateView):
    form_class = OrganizationForm
    template_name = 'projects/plain-form.html'


class NewCourtPopupView(BaseLawyerView, CreatePopupMixin, BaseFormView, CreateView):
    form_class = CourtForm
    template_name = 'projects/plain-form.html'


class NewNationalityPopupView(LoginRequiredMixin, CreatePopupMixin, BaseFormView, CreateView):
    form_class = NationalityForm
    template_name = 'projects/plain-form.html'
